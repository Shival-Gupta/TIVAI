import requests
import os
import logging
import io
from PIL import Image
from logger import image_logger, universal_logger

# Set up API URL and headers
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
HEADERS = {
    "Authorization": "Bearer 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"
}

def query(payload):
    """Send a request to the Hugging Face API and return the image bytes."""
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()  # Raise an error for bad responses
    return response.content

def generate_image(prompt, scene_num):
    """Generate an image using the Hugging Face FLUX AI model."""
    payload = {"inputs": prompt}
    universal_logger.debug(f"Generating image for scene {scene_num}: {prompt}")
    
    try:
        image_bytes = query(payload)  # Get image bytes from API
        image = Image.open(io.BytesIO(image_bytes))  # Open image from bytes

        # Ensure output directory exists
        output_dir = 'output/images'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the image to the specified path
        image_path = os.path.join(output_dir, f"scene_{scene_num}.png")
        image.save(image_path)

        universal_logger.info(f"Image saved: {image_path}")
        image_logger.info(f"Image saved: {image_path}")
        return image_path
    except requests.exceptions.RequestException as e:
        universal_logger.error(f"Error generating image for scene {scene_num}: {e}")
        image_logger.error(f"Error generating image for scene {scene_num}: {e}")
        return None
    except Exception as e:
        universal_logger.exception("An unexpected error occurred while generating the image.")
        return None

if __name__ == "__main__":
    prompt = input("Enter a prompt for the image: ")
    scene_num = 1  # Example scene number
    generate_image(prompt, scene_num)
