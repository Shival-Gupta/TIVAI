# story_generation.py
import subprocess
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG for detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/story_generation.log"),
        logging.StreamHandler()  # Output to terminal
    ]
)

def generate_story(prompt):
    """
    Generate a detailed story, timeline, and image prompts based on the provided prompt.

    Args:
        prompt (str): The story idea provided by the user.

    Returns:
        str: The generated story output or None if generation fails.
    """
    
    # Define the instruction to generate the required output format.
    instruction = (
        "Generate a detailed, vivid, and engaging narrative based on the following story idea. "
        "The response should be structured and separated by the delimiter `=====` in the following order:\n\n"
        "1. **Story**: Write a descriptive story with a clear beginning, middle, and end, focusing on character development, setting, emotions, and significant events.\n\n"
        "2. **Timeline**: Break the story into key scenes or moments in chronological order. For each scene, describe the events and actions with an approximate duration for each scene.\n\n"
        "3. **Image Prompts**: For each important moment in the story, provide creative descriptions for images. Include details like scenery, characters, colors, moods, and objects that would visually represent the scene.\n\n"
        "Use the delimiter `=====` to separate the three sections.\n\n"
        "### Story Idea:\n"
    )

    # Combine the instruction with the user's prompt.
    full_prompt = instruction + prompt

    # Define the command to run the model
    command = ['ollama', 'run', 'llama3.2', full_prompt]

    logging.info(f"Executing command: {' '.join(command)}")

    try:
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the command executed successfully
        if result.returncode != 0:
            logging.error(f"Command failed with return code {result.returncode}.")
            logging.error(f"Error: {result.stderr.strip()}")
            return None  # Return None if command fails

        # Get the output of the command
        output = result.stdout.strip()

        # Print the output for reference
        logging.debug("Generated Output:\n" + output)

        # Save the output in `result.txt`
        os.makedirs('output/text', exist_ok=True)
        with open('output/text/result.txt', 'w') as f:
            f.write(output)

        logging.info("Output saved to output/text/result.txt")
        return output  # Return output for further processing

    except Exception as e:
        logging.exception("An error occurred while generating the story.")
        return None  # Return None on any exception

# If running as a script, get the prompt from the user
if __name__ == "__main__":
    prompt = input("Enter a story idea: ")
    generate_story(prompt)
