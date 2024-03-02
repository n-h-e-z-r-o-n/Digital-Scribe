
from queue import Queue
from threading import Thread
import pyaudio


messages = Queue()
recordings = Queue()

output = []

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




import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    M  =  p.get_device_info_by_index(i)
    print(F" {M['index']}   {M['name']}")

CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 10
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

def record_microphone(chunk=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    input_device_index=0,
                    frames_per_buffer=chunk)

    frames = []

    while not messages.empty():
        data = stream.read(chunk)
        frames.append(data)
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("mic term")


import subprocess
import json
from vosk import Model, KaldiRecognizer
import time

model = Model(model_name="vosk-model-en-us-0.22")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)


def speech_recognition(output):
    print("scanning")
    while not messages.empty():
        frames = recordings.get()

        rec.AcceptWaveform(b''.join(frames))
        result = rec.Result()
        text = json.loads(result)["text"]
        print("----", text)
        #cased = subprocess.check_output('python recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
        #output.append_stdout(cased)
        #time.sleep(1)





start_recording()





