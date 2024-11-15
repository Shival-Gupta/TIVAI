import cv2
import numpy as np
import os
import random

# Functions to generate effects
def pan_right(image, output_path="output.avi", duration=3, fps=12, zoom_scale=1.1, move_x=1):
    frames = []
    num_frames = int(duration * fps)
    for i in range(num_frames):
        zoomed_image = cv2.resize(image, None, fx=zoom_scale, fy=zoom_scale)
        x_offset = int((zoomed_image.shape[1] - image.shape[1]) / 2) - move_x * i
        y_offset = int((zoomed_image.shape[0] - image.shape[0]) / 2)
        pan_frame = zoomed_image[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]]
        frames.append(pan_frame)
    save_video(frames, output_path, fps, image.shape[1], image.shape[0])

def pan_left(image, output_path="output.avi", duration=3, fps=12, zoom_scale=1.1, move_x=-1):
    frames = []
    num_frames = int(duration * fps)
    for i in range(num_frames):
        zoomed_image = cv2.resize(image, None, fx=zoom_scale, fy=zoom_scale)
        x_offset = int((zoomed_image.shape[1] - image.shape[1]) / 2) - move_x * i
        y_offset = int((zoomed_image.shape[0] - image.shape[0]) / 2)
        pan_frame = zoomed_image[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]]
        frames.append(pan_frame)
    save_video(frames, output_path, fps, image.shape[1], image.shape[0])

def pan_up(image, output_path="output.avi", duration=3, fps=12, zoom_scale=1.1, move_y=1):
    frames = []
    num_frames = int(duration * fps)
    for i in range(num_frames):
        zoomed_image = cv2.resize(image, None, fx=zoom_scale, fy=zoom_scale)
        x_offset = int((zoomed_image.shape[1] - image.shape[1]) / 2)
        y_offset = int((zoomed_image.shape[0] - image.shape[0]) / 2) - move_y * i
        pan_frame = zoomed_image[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]]
        frames.append(pan_frame)
    save_video(frames, output_path, fps, image.shape[1], image.shape[0])

def pan_down(image, output_path="output.avi", duration=3, fps=12, zoom_scale=1.1, move_y=-1):
    frames = []
    num_frames = int(duration * fps)
    for i in range(num_frames):
        zoomed_image = cv2.resize(image, None, fx=zoom_scale, fy=zoom_scale)
        x_offset = int((zoomed_image.shape[1] - image.shape[1]) / 2)
        y_offset = int((zoomed_image.shape[0] - image.shape[0]) / 2) - move_y * i
        pan_frame = zoomed_image[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]]
        frames.append(pan_frame)
    save_video(frames, output_path, fps, image.shape[1], image.shape[0])

def zoom_only(image, output_path="output.avi", duration=2.5, fps=24, zoom_start=1.0, zoom_end=1.2):
    frames = []
    num_frames = int(duration * fps)
    zoom_step = (zoom_end - zoom_start) / num_frames
    for i in range(num_frames):
        zoom_scale = zoom_start + zoom_step * i
        zoomed_image = cv2.resize(image, None, fx=zoom_scale, fy=zoom_scale)
        x_offset = int((zoomed_image.shape[1] - image.shape[1]) / 2)
        y_offset = int((zoomed_image.shape[0] - image.shape[0]) / 2)
        zoom_frame = zoomed_image[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]]
        frames.append(zoom_frame)
    save_video(frames, output_path, fps, image.shape[1], image.shape[0])

def save_video(frames, output_path, fps, width, height):
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    print(f"Saved video: {output_path}")

# Apply random effect
def apply_random_effect(image, output_folder, filename):
    effects = [pan_right, pan_left, pan_up, pan_down] + [zoom_only] * 3  # Zoom has higher probability
    effect_function = random.choice(effects)
    output_path = os.path.join(output_folder, f"{filename}.avi")
    effect_function(image, output_path=output_path)

# Combine videos into one
def combine_videos(input_folder, output_path, fps=24):
    video_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.avi')]
    if not video_files:
        print("No video files to combine.")
        return

    # Get the dimensions of the first video
    cap = cv2.VideoCapture(video_files[0])
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"XVID"), fps, (frame_width, frame_height))

    for video_file in video_files:
        cap = cv2.VideoCapture(video_file)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()

    out.release()
    print(f"Combined video saved as: {output_path}")

# Paths
input_folder = r"C:\Users\hp\Desktop\TETOVO\output2"
output_folder = r"C:\Users\hp\Desktop\img_video\video"
combined_video_path = "combined_output.avi"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each image with a random effect
for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png")):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        if image is not None:
            apply_random_effect(image, output_folder, filename.split(".")[0])

# Combine all generated videos
combine_videos(output_folder, combined_video_path)
