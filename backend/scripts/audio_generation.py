from gtts import gTTS
import os

def generate_audio(story):
    # Generate speech from the story
    tts = gTTS(story, lang='en')
    audio_path = "audio/story_audio.mp3"
    tts.save(audio_path)
    return audio_path
