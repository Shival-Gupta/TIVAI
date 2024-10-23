# video_stitching.py
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from logger import video_logger, universal_logger

def merge_videos(video_clips, output_file="output/videos/final_video.mp4"):
    """Merge all video clips into a final video."""
    universal_logger.debug(f"Merging {len(video_clips)} video clips into {output_file}")

    clips = []
    for clip in video_clips:
        try:
            video_clip = VideoFileClip(clip)
            clips.append(video_clip)
            universal_logger.info(f"Loaded video clip: {clip}")
            video_logger.info(f"Loaded video clip: {clip}")
        except Exception as e:
            universal_logger.error(f"Error loading video clip {clip}: {e}")
            video_logger.error(f"Error loading video clip {clip}: {e}")

    if clips:
        final_clip = concatenate_videoclips(clips, method="compose")
        if not os.path.exists('output/videos'):
            os.makedirs('output/videos')
        
        final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
        universal_logger.info(f"Final video created: {output_file}")
        video_logger.info(f"Final video created: {output_file}")
    else:
        universal_logger.error("No video clips to merge.")
        video_logger.error("No video clips to merge.")
