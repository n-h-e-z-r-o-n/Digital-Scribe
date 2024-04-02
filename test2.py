from tkinter import filedialog
filetypes = [("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.aac")]
file_path = filedialog.askopenfilename(filetypes=filetypes)

help(file_path)