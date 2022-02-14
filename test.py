# First we create the class

from manim import *

class CircledSquare(VGroup):
    def __init__(self, square_color = RED, circle_color = BLUE, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.square_color = square_color
        self.circle_color = circle_color
        self.add(Square(color = square_color))
        self.add(Circle(color = circle_color))

class TestScene(Scene):
    def construct(self):
        self.wait()
        self.play(Create(CircledSquare()))
        self.wait()