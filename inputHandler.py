from config import methods

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