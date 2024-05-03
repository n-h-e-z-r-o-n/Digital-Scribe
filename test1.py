import tkinter as tk
from tkinter import ttk
import pygame
import os
import time

class AudioPlayerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Audio Player")

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Audio file path
        self.file_path =r"C:\Users\HEZRON WEKESA\OneDrive\Music\Air I Breathe .mp3"   # Update with your audio file path

        # Load audio file
        pygame.mixer.music.load(self.file_path)

        # Initialize variables for play time tracking
        self.play_time = tk.StringVar()
        self.play_time.set("00:00")

        # Create GUI components
        self.create_widgets()

        # Start tracking play time
        self.track_play_time()

    def create_widgets(self):
        # Play Button
        self.play_button = ttk.Button(self, text="Play", command=self.play_audio)
        self.play_button.pack(pady=10)

        # Stop Button
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_audio)
        self.stop_button.pack(pady=5)

        # Play Time Label
        self.play_time_label = ttk.Label(self, textvariable=self.play_time)
        self.play_time_label.pack()

    def play_audio(self):
        pygame.mixer.music.play()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def track_play_time(self):
        while pygame.mixer.music.get_busy():
            # Get current play time in seconds
            play_time_seconds = pygame.mixer.music.get_pos() / 1000

            # Format play time as MM:SS
            minutes, seconds = divmod(play_time_seconds, 60)
            play_time_formatted = "{:02d}:{:02d}".format(int(minutes), int(seconds))

            # Update play time label
            self.play_time.set(play_time_formatted)

            # Update GUI every second
            self.update_idletasks()
            time.sleep(1)

if __name__ == "__main__":
    app = AudioPlayerApp()
    app.mainloop()
