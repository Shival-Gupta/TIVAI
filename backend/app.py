import time
from scripts.story_generation import generate_story
from scripts.image_generation import generate_images
from scripts.audio_generation import generate_audio
from scripts.video_generation import generate_video

class TIVAIApp:
    def __init__(self):
        self.state = {}
        self.story = None
        self.image_prompts = None
        self.images = None
        self.audio = None
        self.video = None

    def process_prompt(self, prompt):
        print("Processing user prompt...")
        # Step 1: Generate Story & Prompts
        self.story, self.image_prompts, scene_lengths = generate_story(prompt)
        
        # Step 2: Generate Images
        self.images = generate_images(self.image_prompts)
        
        # Step 3: Generate Audio
        self.audio = generate_audio(self.story)
        
        # Step 4: Generate Video
        self.video = generate_video(self.images, self.audio, scene_lengths, self.story)

        return self.video

if __name__ == "__main__":
    tivai_app = TIVAIApp()

    user_prompt = input("Enter your video prompt: ")
    start_time = time.time()
    final_video = tivai_app.process_prompt(user_prompt)
    print("Video generated in", time.time() - start_time, "seconds.")
    # Do something with the final video (e.g., save to output folder)
