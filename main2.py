import os
from dotenv import load_dotenv
from gradio_client import Client

# Load environment variables from .env file
load_dotenv()

# Set the Hugging Face token
hf_token = os.getenv('HF_TOKEN')

# Create a client to interact with the model
client = Client("black-forest-labs/FLUX.1-schnell")

# Define the text prompt and other parameters
result = client.predict(
    prompt='four babies skydiving',  # Example prompt
    seed=0,
    randomize_seed=True,
    width=512,
    height=512,
    num_inference_steps=4,  # Updated parameter name
    api_name="/infer"
)

# Print the result
print(result)

