import os 
import json 
from config import methods
import inputHandler as handler
logo = methods.get_ascii_art()


if __name__ == "__main__":
    methods.check_media_folder()
    methods.display_home()
    handler.handle_intro_input()
    handler.handle_outro_input()
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






