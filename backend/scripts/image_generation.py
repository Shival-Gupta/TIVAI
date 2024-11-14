from diffusers import StableDiffusionPipeline
import torch

# Initialize the Stable Diffusion model
model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original")
model.to("cuda")

def generate_images(prompts):
    images = []
    for prompt in prompts:
        print(f"Generating image for prompt: {prompt}")
        image = model(prompt).images[0]
        images.append(image)
    
    return images
