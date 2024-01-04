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


if __name__ == "__main__":
    methods.display_home()
    handle_intro_input()
    print("Done!")






