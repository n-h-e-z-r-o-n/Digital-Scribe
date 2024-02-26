# pip install assemblyai

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "493cf0249ca34cb39d60fe1effbe307c"


audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

transcriber = aai.Transcriber()

transcript = transcriber.transcribe(audio_url)

print(transcript.text)

print(transcript.words)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")






sentences = transcript.get_sentences()
for sentence in sentences:
  print(sentence.text)

paragraphs = transcript.get_paragraphs()
for paragraph in paragraphs:
  print(paragraph.text)



# Real-Time Transcription











