from pydub import AudioSegment


def convert_wav_to_mp3(wav_file, mp3_file):
    # Load the WAV file
    audio = AudioSegment.from_wav(wav_file)

    # Export the audio as MP3
    audio.export(mp3_file, format="mp3")


convert_wav_to_mp3(r"C:\Users\HEZRON WEKESA\Desktop\python Project\Mental_health Ai\Mental_App\Audio_Records\ (Saturday May 2024,  06 PM).wav", r"C:\Users\HEZRON WEKESA\Desktop\python Project\Mental_health Ai\Mental_App\Audio_Records\ 123.mp3")