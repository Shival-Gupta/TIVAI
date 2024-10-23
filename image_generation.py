import requests
import io
import os
from PIL import Image
from datetime import datetime
import google.generativeai as genai

# Constants and API configurations
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
HUGGINGFACE_API_KEY = "Bearer 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"
GOOGLE_API_KEY = "AIzaSyB_Az0MiidwHv1D47mZfkQCPDJBG_xrbkI"

# Hugging Face API header for Stable Diffusion requests
headers = {"Authorization": HUGGINGFACE_API_KEY}

# Configure Google Generative AI API for text-to-content generation
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Directory to save output images
output_directory = "output_images"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def query_stable_diffusion(payload):
    """Query Hugging Face API to generate an image from a text prompt."""
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to generate image: {response.status_code}, {response.text}")

def generate_image(prompt, index):
    """Generate an image for a specific prompt and save it to the output directory."""
    print(f"Generating image for prompt: '{prompt}'")

    image_bytes = query_stable_diffusion({"inputs": prompt})

    # Create unique filename based on timestamp and index
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"image_{timestamp}_{index + 1}.png"
    file_path = os.path.join(output_directory, file_name)

    # Save the image to the specified directory
    image = Image.open(io.BytesIO(image_bytes))
    image.save(file_path)

    print(f"Image saved at: {file_path}")
    return file_path

def generate_story_from_prompt(prompt):
    """Generate a story outline with image prompts using Google Generative AI."""
    instruction = " Please give me only twelve short, concise, but detailed points that provide a clear picture as output, use ONLY KEYWORDS."
    final_prompt = prompt + instruction

    response = model.generate_content(final_prompt)

    # Clean up response by extracting points
    points = response.text.splitlines()
    points = [point.replace('**', '').strip() for point in points if '**' in point]

    return points

def main():
    # Take user input or use default prompt
    prompt = input("Enter your prompt (default: 'Two friends on a trip to the mountains'): ")
    if not prompt:
        prompt = "Two friends on a trip to the mountains"

    # Step 1: Generate a story outline with image prompts
    points = generate_story_from_prompt(prompt)
    print(f"Generated story outline with {len(points)} scenes.")

    # Step 2: Generate images for each point
    image_paths = []
    for index, point in enumerate(points):
        image_path = generate_image(point, index)
        image_paths.append(image_path)

    print(f"All images generated and saved at: {output_directory}")

if __name__ == "__main__":
    main()
