from typing import Any
from manim import *
import json
import os

from retrieve import get_config

class Intro(Scene):

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


    def generate_titles(self):
        header = Text(self.title, font="Montserrat", color=WHITE).scale(1.5)
        header.to_edge(UP)
        separator = Line(LEFT, RIGHT, color=WHITE).scale(2)
        separator.next_to(header, DOWN)
        subtitle = Text(self.subtitle, font="Montserrat", color=WHITE).scale(1.2)
        subtitle.next_to(separator, DOWN)

        self.play(Write(header))
        self.wait(0.5)
        self.play(Write(separator))
        self.play(Write(subtitle))
        self.wait(1)

    def construct(self):
        self.generate_titles()




def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations)



class Outro(Scene):
    def construct(self):
        text = Text("Thanks for watching!", font="Montserrat", color=WHITE).scale(1.5)
        self.play(Write(text))