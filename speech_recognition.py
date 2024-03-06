import whisper

model = whisper.load_model("base")
result = model.transcribe("12.mp3")
print(result["text"])
