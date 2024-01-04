import os 
import json
import subprocess

# retrieve the ascii art / logo
def get_ascii_art() -> str:
    try:
        file = os.path.join(os.path.dirname(__file__), 'ascii_art.txt')

        with open(file, "r", encoding="utf-8") as file:
            ascii_art_content = file.read()
            return ascii_art_content
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred: {e}")


# retrieve the version
def get_version() -> str:
    try:
        file = os.path.join(os.path.dirname(__file__), 'version.txt')

        with open(file, "r") as file:
            version = file.read()
            return version
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred: {e}")


# change values in the config file 
def change_config(key: str, value) -> None:
    try:
        file = os.path.join(os.path.dirname(__file__), 'config.json')

        with open(file, "r") as f:
            config = json.load(f)
            config[key] = value

        with open(file, "w") as f:
            json.dump(config, f, indent=4)
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred: {e}")


# display the home screen for console app
def display_home() -> None:
    try: 
        ascii_art = get_ascii_art()
        version = get_version()
        print(f"""
{ascii_art}
                    v{version}
\n\n
""")

    except Exception as e:
        print(f"An error occurred: {e}")


