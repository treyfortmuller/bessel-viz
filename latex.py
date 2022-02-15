from manim import *

class AMSLaTeX(Scene):
    def construct(self):
        tex = MathTex(r'x^2 \frac{d^2y}{dx^2} + x \frac{dy}{dx} + (x^2 - \alpha^2)y = 0', font_size=56)
        self.play(Write(tex))
        # text3d = Text("This is a 3D text")
        # self.add_fixed_in_frame_mobjects(tex)
        self.play(tex.animate.scale(0.5))
        self.play(tex.animate.to_corner(UL))


        