from queue import Queue
from threading import Thread
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import subprocess, time
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    M = p.get_device_info_by_index(i)
    print(F" {M['index']}   {M['name']}")


closed = False
import whisper

def RUN_OFFLINE_speech_recognition(widget=None):
    global closed
    messages = Queue()
    recordings = Queue()
    output = []
    FRAME_RATE = 16000
    model = Model(model_name="vosk-model-en-us-0.22")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    def start_recording():
        messages.put(True)
        print("Starting...")
        record = Thread(target=record_microphone)
        record.start()

        transcribe = Thread(target=speech_recognition, args=(output,))
        transcribe.start()

    def stop_recording(data):
        messages.get()
        print("Stopped.")

    def record_microphone(chunk=1024, RECORD_SECONDS=60):
        global closed
        p = pyaudio.PyAudio()
        FRAME_RATE = 16000
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        input_device_index=0,
                        frames_per_buffer=chunk)
        frames = []
        while not messages.empty():
            if closed:
                break
            data = stream.read(chunk)
            frames.append(data)
            if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
                recordings.put(frames.copy())
                frames = []

        stream.stop_stream()
        stream.close()
        p.terminate()


    def speech_recognition(output):
        global closed
        print("scanning")
        while not messages.empty():
            if closed:
                break
            frames = recordings.get()
            save(frames)

            rec.AcceptWaveform(b''.join(frames))
            result = rec.Result()
            text = json.loads(result)["text"]
            if text == "the" or text == "" :
                save(frames)

                continue
            #print("----", text)

    def save(frames):
        # Define audio parameters
        import wave
        channels = 1  # Mono
        sample_width = 2  # 16-bit audio
        sample_rate = 16000  # Sample rate (Hz)
        output_file = 'output.wav'
        # Open the output file in write mode
        with wave.open(output_file, 'wb') as output_wave:
            # Set audio parameters
            output_wave.setnchannels(channels)
            output_wave.setsampwidth(sample_width)
            output_wave.setframerate(sample_rate)

            # Write the audio frames to the file
            output_wave.writeframes(b''.join(frames))

        #print("Audio file saved successfully.")

        model = whisper.load_model("tiny")
        result = model.transcribe(output_file)
        print(result["text"])


    start_recording()


RUN_OFFLINE_speech_recognition()


