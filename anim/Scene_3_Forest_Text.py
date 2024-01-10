from manim import *
from retrieve import get_config

class Scene2(Scene):
    def __init__(self, **kwargs):
        self.init_config()
        super().__init__(**kwargs)

    def init_config (self) -> None:
        try: 
            config = get_config()["intro"]
            self.title = config["title"]
            self.subtitle = config["subtitle"]
        except Exception as e:
            print(e)

    def construct(self):
        title = Text(self.title, font="Montserrat", color=WHITE).scale(1.5)
        title.to_edge(UP)
        title.set_color_by_gradient(BLUE, GREEN, RED)
        separator = Line(LEFT, RIGHT, color=WHITE).scale(2)
        separator.next_to(title, DOWN)
        subtitle = Text(self.subtitle, font="Montserrat", color=WHITE).scale(1.2)
        subtitle.next_to(separator, DOWN)

        group = Group(title, separator, subtitle)
        group.center()

        self.play(Write(title))
        self.wait(0.3)
        self.play(Write(separator))
        self.wait(0.3)
        self.play(Write(subtitle))
