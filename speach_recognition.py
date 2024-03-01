# pip install assemblyai

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "493cf0249ca34cb39d60fe1effbe307c"


audio_url = r"C:\Users\HEZRON WEKESA\Videos\download.mp4"

transcriber = aai.Transcriber()

transcript = transcriber.transcribe(audio_url)

print(transcript.text)

document = (
    "When Apple released the Apple Watch in 2015, it was business as "
    + "usual for a company whose iPhone updates had become cultural "
    + "touchstones. Before the watch went on sale, Apple gave early "
    + "versions of it to celebrities like Beyoncé, featured it in fashion "
    + "publications like Vogue and streamed a splashy event on the "
    + "internet trumpeting its features."
)



"""

print(transcript.words)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")

"""








sentences = transcript.get_sentences()
for sentence in sentences:
  print(sentence.text)

paragraphs = transcript.get_paragraphs()
for paragraph in paragraphs:
  print(paragraph.text)



# Real-Time Transcription











