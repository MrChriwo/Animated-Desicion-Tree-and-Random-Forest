from manim import * 
from retrieve import get_config


class Outro(Scene):
    def __init__(self, **kwargs):
        self.text = get_config()["outro"]
        super().__init__(**kwargs)
    def construct(self):
        text = Text(self.text, font="Montserrat", color=WHITE).scale(1.5)
        self.play(Write(text))