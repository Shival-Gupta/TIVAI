from moviepy.editor import ImageSequenceClip, AudioFileClip, TextClip, concatenate

def generate_video(images, audio_path, scene_lengths, story):
    # Create video clip from images
    image_clip = ImageSequenceClip(images, durations=scene_lengths)
    
    # Load audio
    audio_clip = AudioFileClip(audio_path)
    
    # Sync the audio with the video
    image_clip = image_clip.set_audio(audio_clip)
    
    # Add captions from the story
    text_clips = []
    for idx, scene in enumerate(story.split('.')):
        text_clip = TextClip(scene, fontsize=24, color='white', size=(1920, 1080))
        text_clip = text_clip.set_duration(scene_lengths[idx]).set_position('center').set_start(idx * scene_lengths[idx])
        text_clips.append(text_clip)
    
    final_video = concatenate([image_clip] + text_clips)
    final_video.write_videofile("output/final_video.mp4", codec='libx264')
    
    return "output/final_video.mp4"
