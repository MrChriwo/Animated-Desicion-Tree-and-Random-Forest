import os 
import json 
from config import methods
logo = methods.get_ascii_art()


def handle_intro_input() -> None: 
    valid = False
    struct = {"title": "", "subtitle": ""}
    try: 
        while not valid:
            title = input("Enter title: ")
            if title == "":
                continue
            struct["title"] = title

            subtitle = input("Enter subtitle: ")
            if subtitle == "":
                continue
            struct["subtitle"] = subtitle
            valid = True
        methods.change_config("intro", struct)
    except Exception as e:
        print(e)
        print("Error while handling intro input.")


def handle_outro_input() -> None: 
    valid = False
    text = ""
    try: 
        while not valid:
            title = input("Enter outro text: ")
            if title == "":
                continue
            text = title
            valid = True
        methods.change_config("outro", text)
    except Exception as e:
        print(e)
        print("Error while handling intro input.")



if __name__ == "__main__":
    methods.check_media_folder()
    methods.display_home()
    handle_intro_input()
    handle_outro_input()
    quals = ["low", "medium", "high", "ultra"]
    while True:
        quality = input("Enter quality: (low | medium | high | ultra): ")
        if quality in quals:
            break
        else:
            print("Invalid input.")
    
    input("Press enter to start building video...")
    
    methods.build_video(quality=quality)
    methods.play_video()
    print("\n\nProject created. video available at anim/output.mp4")

    print("Done!")






