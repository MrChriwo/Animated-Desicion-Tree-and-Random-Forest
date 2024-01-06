from manim import * 
import os

class a_introduce_bob(Scene):
    
        def __init__(self, **kwargs):
            self.asset_path = os.path.join(os.getcwd(), "assets", "intro")
            super().__init__(**kwargs)
    
            
        def construct(self):
            # make scene background blue (same color as bank bg to make it look like it's the same scene)
            self.camera.background_color = "#BEEBF1"

            bank_asset = os.path.join(self.asset_path, "bank.jpg")
            bob_asset = os.path.join(self.asset_path, "bob.png")
            bank_employee = ImageMobject(bank_asset)
            bob = ImageMobject(bob_asset)
            header = Text("Bob", font="Montserrat", color=BLACK).scale(1.5)
            header.to_edge(UP)
            bob.next_to(header, DOWN)

            group = Group(bob, header)
            # move bob a bit upper to make a fluent animation with the bank
            group[0].shift(UP*1.2)
            group.center()

            # fade in bob
            self.play(FadeIn(group[0]))
            self.wait(0.8)
            # write the header text (bob)
            self.play(Write(group[1]))
            self.wait(1)
            # fade in the bank "background"
            self.play(FadeIn(bank_employee))
            self.wait(3)


class b_bob_and_customers(Scene):
        
        def __init__(self, **kwargs):
            self.asset_path = os.path.join(os.getcwd(), "assets", "intro")
            super().__init__(**kwargs)

        def construct(self):
            self.camera.background_color = "#BEEBF1"

            bank_asset = os.path.join(self.asset_path, "bank.jpg")
            bank_employee = ImageMobject(bank_asset)
            self.play(bank_employee.animate.scale(0.7).shift(LEFT*3))




