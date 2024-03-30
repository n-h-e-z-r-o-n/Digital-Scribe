import whisper

model = whisper.load_model("base")
print('starting')
result = model.transcribe("12.mp3")
print(result["text"])
result = model.transcribe(indata_transformed, language=LANGUAGE)