from typing import Any
from manim import *
from retrieve import get_config, split_gif
import os

class ForestScene(Scene):

    def __init__(self, **kwargs):
        self.asset_path = os.path.join(os.getcwd(), "assets", "intro")
        super().__init__(**kwargs)

    def create_background(self): 
        # list images in frames folder
        gif = os.path.join(self.asset_path, "forest_generating.gif")
        frame_iterator = split_gif(gif)

        try:
            while True: 
                frame = next(frame_iterator)
                image = ImageMobject(frame)
                self.add(image) 
                self.wait(0.1)
        except StopIteration:
            pass

    def construct(self):
        self.create_background()
        self.play(FadeOut(*self.mobjects))
        self.wait(0.5)
        
        

