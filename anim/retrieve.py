import json
import os
import imageio
from PIL import Image

# retrieve the config file
def get_config() -> dict:
    try:
        file = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

        with open(file, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred: {e}")



def split_gif(gif_path):

    images = imageio.get_reader(gif_path)
    for i, frame in enumerate(images):

        frame = Image.fromarray(frame)
        resized_frame = frame.resize((1920, 1080), Image.ANTIALIAS)
        yield resized_frame
