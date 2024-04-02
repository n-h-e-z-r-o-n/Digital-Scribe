from tkinter import filedialog
filetypes = [("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.aac")]
file_path = filedialog.askopenfilename(filetypes=('mp3'))

help(file_path)