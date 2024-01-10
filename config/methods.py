import os 
import json
import subprocess
import shutil

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



# helping function for concat_video
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

    # sort mp4_files by name
    mp4_files.sort()
    return mp4_files



def create_video(quality: str) -> None:
    quality_flag = ""
    if quality == "low":
        quality_flag = "-ql"
    elif quality == "medium":
        quality_flag = "-qm"
    elif quality == "high":
        quality_flag = "-qh"
    elif quality == "ultra":
        quality_flag = "-qk"
    else: 
        print("Invalid quality flag. Using default quality flag.")
        quality_flag = "-ql"
    try:
        # get all pyscripts from the anim folder
        files = os.listdir(os.path.join(os.path.dirname(__file__), "..", "anim"))
        files = [file for file in files if file.endswith(".py") and file != "retrieve.py"]
        
        # compile all the files
        for file in files:
            subprocess.run(["manim", quality_flag, file, "-a"], cwd=os.path.join(os.path.dirname(__file__), "..", "anim"))

    except Exception as e:
        print(f"An error occurred: {e}")
    
# concatenate the videos 
def concat_videos () -> None:
    try:
        files = get_all_videos()
        anim_folder = os.path.join(os.path.dirname(__file__), "..", "anim")
        tmp_compile_file = os.path.join(anim_folder, "tmp.txt")

        with open(tmp_compile_file, "w") as f:
            for file in files:
                f.write(f"file '{file}'\n")
        # run the ffmpeg command
                
        # if anim/output.mp4 exists, delete it
        if os.path.exists(os.path.join(anim_folder, "output.mp4")):
            os.remove(os.path.join(anim_folder, "output.mp4"))

        subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", tmp_compile_file, "-c", "copy", "output.mp4"], cwd=os.path.join(os.path.dirname(__file__), "..", "anim"))
        os.remove(tmp_compile_file)
    except Exception as e:
        print(f"An error occurred: {e}") 



def add_audio() -> None:
    try:    
    # run ffmpeg -i video.mkv -i audio.mp3 -map 0 -map 1:a -c:v copy -shortest output.mkv
        subprocess.run(["ffmpeg", "-i", "output.mp4", "-i", "background_track.mp3", "-map", "0", "-map", "1:a", "-c:v", "copy", "-shortest", "output2.mp4"], cwd=os.path.join(os.path.dirname(__file__), "..", "anim"))


    except Exception as e:
        print(f"An error occurred: {e}")

def play_video() -> None:
    video_height = 800
    video_width = 1200
    try:
        subprocess.run(["ffplay", "-x", str(video_width), "-y", str(video_height), "output.mp4"], cwd=os.path.join(os.path.dirname(__file__), "..", "anim"))
    except Exception as e:
        print(f"An error occurred: {e}")


def check_media_folder() -> None:
        if os.path.exists(os.path.join(os.path.dirname(__file__), "..", "anim", "media")):
            shutil.rmtree(os.path.join(os.path.dirname(__file__), "..", "anim", "media"))

def build_video(quality: str) -> None:
    try:
        create_video(quality=quality)
        concat_videos()
        add_audio()
    except Exception as e:
        print(f"An error occurred: {e}")
