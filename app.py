import os
import subprocess
import requests
import io
import streamlit as st
from dotenv import load_dotenv
import openai
from gtts import gTTS
from PIL import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, AudioFileClip
import time
import logging

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Constants
OUTPUT_DIR = "output"
TEXT_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "text")
IMAGE_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "images")
VIDEO_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "videos")
DEFAULT_PROMPT = "chicken biryani tutorial"

# Streamlit App Setup
st.title("TIVAI (Text-to-Image-to-Video using AI)")

# Create necessary directories
os.makedirs(TEXT_OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

# Input Fields
prompt = st.text_input("Enter a short prompt for video generation:", DEFAULT_PROMPT)
model_choice = st.selectbox("Choose model for story generation:", ["llama3.2 (local)", "llama3.1 (local)"])
aspect_ratio = st.selectbox("Choose aspect ratio:", ["16:9", "3:4", "1:1"])
want_speech = st.checkbox("Generate Speech/Audio?", value=True)
num_scenes = st.slider("Number of scenes:", 1, 10, 5)

# Progress bar
progress_bar = st.progress(0)

# Initialize logging
logging.basicConfig(filename='tivai.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Helper Functions
def display_status(task, status):
    st.write(f"{task}: **{status}**")
    logging.info(f"{task}: {status}")

# Initial Story Generation Function
def generate_initial_story(prompt, model_choice, num_scenes):
    display_status(f"Initial story generation using {model_choice}", "started")
    story = []

    # Construct the initial prompt for AI to generate broad tutorial content
    initial_prompt = f"""
    You are an expert tutorial creator. Your task is to generate a detailed story script for a tutorial video. 
    The tutorial is about: **{prompt}**.
    The video will be divided into {num_scenes} scenes, and each scene will have:
    1. A basic **description** of what happens in the scene.
    2. A **brief explanation** of what the audience will learn or see in that part of the video.

    Each scene will describe the general process of the tutorial, breaking it down into manageable steps.

    For each scene, provide:
    - A short description of what happens in the scene.
    - A brief explanation of what is happening in the tutorial.
    """

    try:
        # Generate content using local or OpenAI models
        if "local" in model_choice:
            model_name = model_choice.split()[0].lower()
            command = ['ollama', 'run', model_name, initial_prompt]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr.strip())
            output = result.stdout.strip()

        elif model_choice == "OpenAI (API)":
            openai.api_key = OPENAI_API_KEY
            response = openai.Completion.create(
                engine="text-davinci-003", prompt=initial_prompt, max_tokens=500
            )
            output = response.choices[0].text.strip()

        elif model_choice == "Gemini (API)":
            headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
            data = {"prompt": initial_prompt}
            response = requests.post("https://api.gemini.ai/v1/generate", headers=headers, json=data)
            if response.status_code != 200:
                raise Exception(f"Gemini API Error: {response.status_code}")
            output = response.json().get('text', "")

        else:
            st.error("Invalid model choice!")
            return None

        story.append(output)

        display_status(f"Initial story generation using {model_choice}", "completed")
        return story

    except Exception as e:
        display_status(f"Initial story generation using {model_choice}", f"failed with error: {e}")
        st.error(f"Error in initial story generation: {e}")
        return None

# Refactor Story Function (Second AI Prompt)
def refactor_story(initial_story, model_choice):
    display_status("Refactoring story", "started")

    # Construct the refactor prompt to organize and refine the generated content
    refactor_prompt = f"""
    You are an expert script editor. The following is a rough draft for a tutorial video about **{prompt}**:
{initial_story}

Your task is to **refactor** the story and structure it in the following format:
- Scene 1: **Image Prompt** + **Audio Transcript** (short, clear narration script).
- Scene 2: **Image Prompt** + **Audio Transcript**, etc.

Ensure that the tutorial is structured with clear, actionable steps. 
- Break down each scene into a detailed **image prompt** (describing what visuals should appear).
- Add a corresponding **audio transcript** that clearly narrates the action.

Your output should contain the refactored story, divided into scenes as per the above structure. Each scene should be separated by "#@$#", and each scene should contain the image prompt and audio transcript separated by "#*8#".

For example:
Scene 1: 
Image Prompt: [Description of the visuals for Scene 1]
#*8#
Audio Script: [Narration for Scene 1]
#@$#
Scene 2: 
Image Prompt: [Description of the visuals for Scene 2]
#*8#
Audio Script: [Narration for Scene 2]
#@$#

...and so on for each scene.

    """

    try:
        # Generate the refactored content using AI
        if "local" in model_choice:
            model_name = model_choice.split()[0].lower()
            command = ['ollama', 'run', model_name, refactor_prompt]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr.strip())
            output = result.stdout.strip()

        elif model_choice == "OpenAI (API)":
            openai.api_key = OPENAI_API_KEY
            response = openai.Completion.create(
                engine="text-davinci-003", prompt=refactor_prompt, max_tokens=1000
            )
            output = response.choices[0].text.strip()

        elif model_choice == "Gemini (API)":
            headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
            data = {"prompt": refactor_prompt}
            response = requests.post("https://api.gemini.ai/v1/generate", headers=headers, json=data)
            if response.status_code != 200:
                raise Exception(f"Gemini API Error: {response.status_code}")
            output = response.json().get('text', "")

        else:
            st.error("Invalid model choice!")
            return None

        # Save the refactored output into a file
        with open(os.path.join(TEXT_OUTPUT_DIR, 'refactored_story.txt'), 'w') as f:
            f.write(output)

        display_status("Refactoring story", "completed")
        return output

    except Exception as e:
        display_status("Refactoring story", f"failed with error: {e}")
        st.error(f"Error in story refactoring: {e}")
        return None

# Image Generation Function
def generate_image(prompt, scene_num):
    display_status(f"Image generation for scene {scene_num}", "started")
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    retries = 3  # Number of retries in case of a rate limit error
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)

            if response.status_code == 429:  # Rate limit reached
                if attempt < retries - 1:  # Don't wait on last attempt
                    time.sleep(3)
                    continue
                else:
                    raise Exception("Rate limit reached, please try again later.")

            if response.status_code != 200:
                raise Exception(f"Error generating image: {response.text}")

            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image_path = os.path.join(IMAGE_OUTPUT_DIR, f"scene_{scene_num}.png")
            image.save(image_path)

            display_status(f"Image generation for scene {scene_num}", "completed")
            return image_path

        except Exception as e:
            display_status(f"Image generation for scene {scene_num}", f"failed: {e}")
            st.error(f"Error generating image for scene {scene_num}: {e}")
            return None

# Audio Generation Functions
def generate_audio_transcript(script, scene_num):
    display_status(f"Audio generation for scene {scene_num}", "started")
    try:
        tts = gTTS(script, lang='en')
        audio_path = os.path.join(OUTPUT_DIR, f"scene_{scene_num}.mp3")
        tts.save(audio_path)

        display_status(f"Audio generation for scene {scene_num}", "completed")
        return audio_path
    except Exception as e:
        display_status(f"Audio generation for scene {scene_num}", f"failed: {e}")
        st.error(f"Error generating audio for scene {scene_num}: {e}")
        return None

# Video Creation Function
def create_video_from_images_audio(image_paths, audio_paths, video_file_name="final_video.mp4"):
    display_status("Creating video", "started")
    try:
        clips = []

        for i in range(len(image_paths)):
            image = ImageClip(image_paths[i])
            audio = AudioFileClip(audio_paths[i])

            # Adjust duration to match audio length
            image = image.set_duration(audio.duration)

            # Set audio
            image = image.set_audio(audio)

            clips.append(image)

        # Concatenate all video clips
        final_video = concatenate_videoclips(clips)

        # Export final video
        video_path = os.path.join(VIDEO_OUTPUT_DIR, video_file_name)
        final_video.write_videofile(video_path, codec="libx264", fps=24)

        display_status("Creating video", "completed")
        return video_path
    except Exception as e:
        display_status("Creating video", f"failed: {e}")
        st.error(f"Error creating video: {e}")
        return None

# Main Workflow
if st.button("Generate Tutorial Video"):
    progress_bar.progress(20)

    # Step 1: Generate initial story
    story = generate_initial_story(prompt, model_choice, num_scenes)
    if story is None:
        st.error("Failed to generate story!")
        progress_bar.progress(0)
        st.stop()

    progress_bar.progress(40)
    st.write("Initial story generated. Refactoring into scenes...")

    # Step 2: Refactor story into scenes
    refactored_story = refactor_story(story[0], model_choice)
    if refactored_story is None:
        st.error("Failed to refactor story!")
        progress_bar.progress(0)
        st.stop()

    progress_bar.progress(60)
    st.write("Story refactored. Generating images and audio...")

    # Step 3: Generate images and audio
    image_paths = []
    audio_paths = []

    # Split the refactored story into scenes using the "#@$#" delimiter
    scenes = refactored_story.split("#@$#")

    for idx, scene in enumerate(scenes):
        st.write(f"Generating for Scene {idx+1}")
        scene_content = scene.strip()

        # Split the scene into image prompt and audio script using the "#*8#" delimiter
        if "#*8#" in scene_content:
            image_prompt, audio_script = scene_content.split("#*8#")

            # Generate image for the scene
            image_path = generate_image(image_prompt.strip(), idx + 1)
            if image_path:
                image_paths.append(image_path)

            # Generate audio for the scene if the user wants it
            if want_speech:
                audio_path = generate_audio_transcript(audio_script.replace("Audio Transcript:", "").strip(), idx + 1)
                if audio_path:
                    audio_paths.append(audio_path)

    progress_bar.progress(80)

    # Step 4: Create final video
    if len(image_paths) > 0:
        video_path = create_video_from_images_audio(image_paths, audio_paths)
        if video_path:
            st.success("Video created successfully!")
            st.video(video_path)
            progress_bar.progress(100)

        # Clean up
        for path in image_paths + audio_paths:
            os.remove(path)


