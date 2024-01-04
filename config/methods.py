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



# create videos from all scenes
def create_videos(quality= "medium") -> None:
    if quality == "low":
        quality = "-ql"
    elif quality == "medium":
        quality = "-qm"
    elif quality == "high":
        quality = "-qh"
    elif quality == "ultra": # 4k rendering 
        quality = "-qk"

    try:
        # get all pyscripts from the anim folder(all scenes actually)
        files = os.listdir(os.path.join(os.path.dirname(__file__), "..", "anim"))
        files = [file for file in files if file.endswith(".py")]
        
        # compile all scenes
        for file in files:
            subprocess.run(["manim", {quality}, file, "-a"], cwd=os.path.join(os.path.dirname(__file__), "..", "anim"))

    except Exception as e:
        print(f"An error occurred: {e}")


# helping function for concat_videos
def get_all_videos(): 
    cwd = os.getcwd()
    anim_video_folder = os.path.join(cwd, "anim", "media", "videos")
    mp4_files = []

    for root, dirs, files in os.walk(anim_video_folder):
        for file in files:
            if file.endswith(".mp4"):
                # cut the path of file until anim
                file = os.path.join(root, file).split("anim")[1]
                if "partial_movie_files" not in file:
                    mp4_files.append(file)
    return mp4_files

    
# concatenate all scenes together    
def concat_videos () -> None:
    try:
        files = get_all_videos() # all mp4 files 
        anim_folder = os.path.join(os.path.dirname(__file__), "..", "anim")
        tmp_compile_file = os.path.join(anim_folder, "tmp.txt")

        with open(tmp_compile_file, "w") as f:
            for file in files:
                f.write(f"file '{file}'\n")

        # concatenate all videos using ffmpeg
        subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", tmp_compile_file, "-c", "copy", "output.mp4"], cwd=os.path.join(os.path.dirname(__file__), "..", "anim"))
        
        # remove the tmp file
        os.remove(tmp_compile_file)

    except Exception as e:
        print(f"An error occurred while concatenating the videos: {e}") 

