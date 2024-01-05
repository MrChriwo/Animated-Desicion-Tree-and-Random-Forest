from manim import *


class Scene2(Scene):
    def construct(self):
        text = Text("Scene 2", font="Montserrat", color=WHITE).scale(1.5)
        self.play(Write(text))
        self.wait(1)
        self.play(FadeOut(text))