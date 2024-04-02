# Example code (not functional, for illustration purposes)
import pyannote.audio as pa

# Load your audio file (e.g., 'audio.wav')
audio = pa.AudioFile("audio.wav")

# Create a speaker diarization pipeline
diarization_pipeline = pa.SpeakerDiarization()

# Process the audio
diarization = diarization_pipeline(audio)

# Get speaker segments
for segment, speaker in diarization.itertracks(yield_label=True):
    print(f"Speaker {speaker} speaks from {segment.start:.2f}s to {segment.end:.2f}s")