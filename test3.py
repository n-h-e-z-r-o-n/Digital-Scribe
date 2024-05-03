import tkinter as tk
import pygame

def play_audio(file_path):

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

def main():
    pygame.mixer.init()
    root = tk.Tk()
    root.title("Audio Player")

    file_path = r"C:\Users\HEZRON WEKESA\OneDrive\Music\Air I Breathe .mp3"  # Update with your audio file path

    play_button = tk.Button(root, text="Play", command=lambda: play_audio(file_path))
    play_button.pack()

    stop_button = tk.Button(root, text="Stop", command=stop_audio)
    stop_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
