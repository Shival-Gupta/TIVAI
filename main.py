# main.py
import os
import re
import logging
from story_generation import generate_story
from image_generation import generate_image
from video_generation import animate_image
from video_stitching import merge_videos

# Constants
OUTPUT_DIR = "output"
TEXT_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "text")
DEFAULT_PROMPT = "Two friends on a trip to the mountains"

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG for detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/main.log"),
        logging.StreamHandler()  # Output to terminal
    ]
)

# Create necessary output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEXT_OUTPUT_DIR, exist_ok=True)

def loading_message(message):
    """Display a loading message in terminal and log it."""
    print(f"\n[[{message}]]", flush=True)
    logging.info(message)  # Log the message for detailed logs

def main():
    """
    Main function to execute the story generation and video creation process.
    It prompts the user for a story idea, generates the story and associated media,
    and merges them into a video.
    """
    prompt = input(f"Enter a video prompt (default: '{DEFAULT_PROMPT}'): ") or DEFAULT_PROMPT
    logging.info(f"[PROMPT]: {prompt}")

    # Step 1: Generate Story and Image Prompts
    loading_message("Generating story, timeline, and image prompts")
    output = generate_story(prompt)

    logging.debug("Full Output:\n" + output)  # Log full output for debugging

    # Guard clause for empty output
    if not output:
        logging.error("Story generation failed. Exiting.")
        print("Story generation failed. Exiting.")
        return

    # Split output into story, timelines, and image prompts using regex
    try:
        parts = re.split(r'={3,}', output)  # Regex to match three or more equals signs
        if len(parts) >= 3:
            story = parts[0].strip()
            timelines = parts[1].strip()
            image_prompts = parts[2].strip()
        else:
            raise ValueError("Output does not contain enough sections.")
    except ValueError as e:
        logging.error(f"Error: {e}. Unable to unpack story, timeline, and image prompts.")
        print("Error: Output format is incorrect. Unable to unpack story, timeline, and image prompts.")
        return

    # Display only essential parts on the terminal
    print("\nStory generated:\n", story)
    print("\nTimelines generated:\n", timelines)

    video_clips = []

    # Step 2: Generate Images for Each Scene
    for idx, scene_prompt in enumerate(image_prompts.strip().splitlines(), start=1):
        loading_message(f"Generating image for scene {idx}")
        image_path = generate_image(scene_prompt.strip(), idx)
        if image_path:
            # Step 3: Animate Each Image
            loading_message(f"Animating image for scene {idx}")
            animated_clip = animate_image(image_path, idx)
            video_clips.append(animated_clip)
        else:
            logging.error(f"Skipping scene {idx} due to image generation error.")
            print(f"Skipping scene {idx} due to image generation error.")  # Log to terminal

    # Step 4: Merge Video Clips
    if video_clips:
        loading_message("Merging video clips")
        merge_videos(video_clips)
        logging.info("Video clips merged successfully.")
    else:
        logging.warning("No video clips generated for merging.")

if __name__ == "__main__":
    main()
