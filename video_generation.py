# video_generation.py
import cv2
import os
from logger import video_logger, universal_logger

def animate_image(image_path, scene_num):
    """Animate an image and save it as a video clip."""
    universal_logger.debug(f"Animating image for scene {scene_num}: {image_path}")
    
    # Animation parameters
    video_path = f"output/videos/animated_scene_{scene_num}.mp4"
    width, height = 640, 480  # Dimensions of the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_path, fourcc, 30.0, (width, height))
    
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (width, height))

    # Create a simple animation by writing the same image for 30 frames
    for _ in range(30):
        video.write(image)

    video.release()
    universal_logger.info(f"Animation completed for scene {scene_num}. Video saved: {video_path}")
    video_logger.info(f"Animation completed for scene {scene_num}. Video saved: {video_path}")
    return video_path
