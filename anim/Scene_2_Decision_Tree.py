from manim import *

class a_decision_tree_intro(Scene):
    def construct(self):
        self.wait(0.5)
        title = Text("Decision Trees", font="Montserrat", color=WHITE).scale(1.5)
        title.to_edge(UP)
        separator = Line(LEFT, RIGHT, color=WHITE).scale(2)
        separator.next_to(title, DOWN)

        group = Group(title, separator)
        group.center()

        self.play(Write(title))
        self.wait(0.3)
        self.play(Write(separator))
        self.wait(0.3)
        self.play(FadeOut(*self.mobjects))
