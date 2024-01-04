import json
import os

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