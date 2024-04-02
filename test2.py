from tkinter import filedialog
import whisper


filetypes = [("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.aac")]
file_path = filedialog.askopenfilename(filetypes=filetypes)
model = whisper.load_model("base")
print(filetypes)
result = model.transcribe("file_path")
print(result["text"])

help(file_path)