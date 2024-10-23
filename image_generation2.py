import os
import logging
from PIL import Image
from diffusers import DiffusionPipeline
from logger import image_logger, universal_logger

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
OUTPUT_DIR = 'output/images'

def load_pipeline(model_name: str) -> DiffusionPipeline:
    """Load the diffusion pipeline model from Hugging Face.

    Args:
        model_name (str): The name of the model to load.

    Returns:
        DiffusionPipeline: The loaded model pipeline.
    
    Raises:
        Exception: If the model loading fails.
    """
    try:
        universal_logger.info(f"Loading model: {model_name}")
        pipe = DiffusionPipeline.from_pretrained(model_name)
        universal_logger.info("Model loaded successfully.")
        return pipe
    except Exception as e:
        universal_logger.error(f"Failed to load model {model_name}: {e}")
        raise

def generate_image(pipe: DiffusionPipeline, prompt: str, scene_num: int) -> str:
    """Generate an image using the Hugging Face FLUX AI model and save it to disk.
    
    Args:
        pipe (DiffusionPipeline): The diffusion pipeline for image generation.
        prompt (str): The prompt for image generation.
        scene_num (int): The scene number for naming the output image file.

    Returns:
        str: The file path of the saved image or None if an error occurred.
    """
    universal_logger.debug(f"Generating image for scene {scene_num}: {prompt}")
    
    try:
        # Generate the image using the pipeline
        result = pipe(prompt)
        image = result.images[0]  # Extract the first image from the result

        # Save the image
        return save_image(image, scene_num)
    except Exception as e:
        universal_logger.error(f"Error generating image for scene {scene_num}: {e}")
        image_logger.error(f"Error generating image for scene {scene_num}: {e}")
    return None

def save_image(image: Image.Image, scene_num: int) -> str:
    """Save the generated image to disk.
    
    Args:
        image (Image.Image): The image to save.
        scene_num (int): The scene number for naming the output image file.

    Returns:
        str: The file path of the saved image.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists
    image_path = os.path.join(OUTPUT_DIR, f"scene_{scene_num}.png")
    image.save(image_path)

    universal_logger.info(f"Image saved: {image_path}")
    image_logger.info(f"Image saved: {image_path}")
    return image_path

def main():
    """Main function to execute the image generation."""
    prompt = input("Enter a prompt for the image: ")
    scene_num = 1  # Example scene number

    # Load the model
    pipe = load_pipeline(MODEL_NAME)

    # Generate and save the image
    generate_image(pipe, prompt, scene_num)

if __name__ == "__main__":
    main()
