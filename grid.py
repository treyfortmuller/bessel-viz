from manim import *

class ExampleBoxes(Scene):
    def construct(self):
        boxes=VGroup(*[Square() for s in range(0,6)])
        boxes.arrange_in_grid(rows=2, buff=1)
        self.add(boxes)