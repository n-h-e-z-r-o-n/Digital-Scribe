import socket
import pyaudio
import threading

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("41.90.178.144", 12345))

# Initialize PyAudio for audio playback
audio = pyaudio.PyAudio()
send_audio_f = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
received_audio_f  = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)


def receive_audio():
    while True:
        audio_data = client_socket.recv(1024)
        received_audio_f.write(audio_data)  # Play the audio data



def send_audio():
    while True:
        audio_data = send_audio_f.read(1024)
        client_socket.send(audio_data)


rev_threading = threading.Thread(target=receive_audio)
send_threading = threading.Thread(target=send_audio)


rev_threading.start()
send_threading.start()
