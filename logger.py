# logger.py
import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with a specified name and log file."""
    # Create the logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Universal Logger
universal_logger = setup_logger('universal', 'logs/main.log', logging.DEBUG)

# Individual Loggers
story_logger = setup_logger('story_generation', 'logs/story_generation.log', logging.DEBUG)
image_logger = setup_logger('image_generation', 'logs/image_generation.log', logging.DEBUG)
video_logger = setup_logger('video_generation', 'logs/video_generation.log', logging.DEBUG)
stitching_logger = setup_logger('video_stitching', 'logs/video_stitching.log', logging.DEBUG)
