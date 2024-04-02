from tkinter import filedialog
import whisper


filetypes = [("Audio Files", "*.mp3;*.wav;*.mpeg;*.mpga;*.mp4;*.webm;*.m4a")]
file_path = filedialog.askopenfilename(filetypes=filetypes)
print(file_path)

model = whisper.load_model("tiny")

result = model.transcribe(rf"{file_path}")
print(result["text"])

help(file_path)