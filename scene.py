from manim import *
from functools import partial
from scipy import special

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        text = Text("Hello world", font="monospace", font_size=64)
        
        # self.add(text)
        self.play(Write(text))
        self.play(text.animate.scale(0.5), run_time=1)
        self.play(text.animate.shift(3*UP))
        self.wait(1)

        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
        self.wait(1)

class SomeOtherSurface(ThreeDScene):
    def construct(self):
        resolution_fa = 42
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        def param_gauss(sig, u, v):
            x = u
            y = v
            sigma, mu = sig, [0.0, 0.0]
            d = np.linalg.norm(np.array([x - mu[0], y - mu[1]]))
            z = np.exp(-(d ** 2 / (2.0 * sigma ** 2)))
            return np.array([x, y, z])

        gauss_plane_0 = Surface(
            partial(param_gauss, 0.5),
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2]
        )
        
        gauss_plane_1 = Surface(
            partial(param_gauss, 0.1),
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2]
        )

        gauss_plane_0.scale(2, about_point=ORIGIN)
        gauss_plane_0.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane_0.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        gauss_plane_1.scale(2, about_point=ORIGIN)
        gauss_plane_1.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane_1.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        self.add(axes,gauss_plane_0)
        self.wait(1)

        self.play(Transform(gauss_plane_0, gauss_plane_1), run_time=3)
        self.wait(1)

        self.stop_ambient_camera_rotation()

class ParaSurface(ThreeDScene):
    def func(self, u, v):
        r = u
        phi = v
        return np.array([r * np.cos(phi), r * np.sin(phi), r])

    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[0, 1],
            v_range=[0, 2*PI]
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes, surface)

class BesselSurface(Surface):
    def __init__(self, boundary, order, mode):
        self.boundary = boundary
        self.order = order
        self.mode = mode

        super().__init__(
            self.func,
            u_range=[0, self.boundary],
            v_range=[0, 2*PI]
        )

    def modal_freq(self):
        # grab the zero for the mode and order that we care about
        zero = special.jn_zeros(self.order, self.mode)[self.mode - 1]
        return zero / self.boundary

    def func(self, u, v):
        r, phi = u, v
        z = special.jv(self.order, self.modal_freq() * r) * np.cos(self.order * phi),
        return np.array([r * np.cos(phi), r * np.sin(phi), z[0]])


class BesselScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        surface = BesselSurface(1, 1, 2)
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes, surface)


# class Vibrate(Animation):
#     def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
#         # Pass number as the mobject of the animation
#         super().__init__(number,  **kwargs)
#         # Set start and end
#         self.start = start
#         self.end = end

#     def interpolate_mobject(self, alpha: float) -> None:
#         # Set value of DecimalNumber according to alpha
#         value = self.start + (alpha * (self.end - self.start))
#         self.mobject.set_value(value)


# class CountingScene(Scene):
#     def construct(self):
#         # Create Decimal Number and add it to scene
#         number = DecimalNumber().set_color(WHITE).scale(5)
#         # Add an updater to keep the DecimalNumber centered as its value changes
#         number.add_updater(lambda number: number.move_to(ORIGIN))

#         self.add(number)

#         self.wait()

#         # Play the Count Animation to count from 0 to 100 in 4 seconds
#         self.play(Count(number, 0, 100), run_time=4, rate_func=linear)

#         self.wait()