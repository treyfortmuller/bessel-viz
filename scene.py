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
        self.play(text.animate.shift(3 * UP))
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
            z = np.exp(-(d**2 / (2.0 * sigma**2)))
            return np.array([x, y, z])

        gauss_plane_0 = Surface(
            partial(param_gauss, 0.5),
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2],
        )

        gauss_plane_1 = Surface(
            partial(param_gauss, 0.1),
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2],
        )

        gauss_plane_0.scale(2, about_point=ORIGIN)
        gauss_plane_0.set_style(fill_opacity=1, stroke_color=GREEN)
        gauss_plane_0.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        gauss_plane_1.scale(2, about_point=ORIGIN)
        gauss_plane_1.set_style(fill_opacity=1, stroke_color=GREEN)
        gauss_plane_1.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        self.add(axes, gauss_plane_0)
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
            lambda u, v: axes.c2p(*self.func(u, v)), u_range=[0, 1], v_range=[0, 2 * PI]
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes, surface)


class BesselSurface(Surface):
    def __init__(self, boundary, order, mode):
        self.boundary = boundary
        self.order = order
        self.mode = mode

        # the time dimension by which to animate the vibrations
        self.t = 0

        super().__init__(self.func, u_range=[0, self.boundary], v_range=[0, 2 * PI])

    def modal_freq(self):
        # grab the zero for the mode and order that we care about
        zero = special.jn_zeros(self.order, self.mode)[self.mode - 1]
        return zero / self.boundary

    def set_time(self, delta_time):
        self.t += delta_time
        # super().__init__(self.func, u_range=[0, self.boundary], v_range=[0, 2 * PI])


    def func(self, u, v):
        r, phi = u, v
        z = (
            special.jv(self.order, self.modal_freq() * r)
            * np.cos(self.order * phi)
            * np.cos(self.modal_freq() * self.t)
        )
        return np.array([r * np.cos(phi), r * np.sin(phi), z])


# class BesselScene(ThreeDScene):
#     def construct(self):
#         axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
#         surface = BesselSurface(1, 1, 2)
#         self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
#         self.add(axes, surface)


# class Vibrate(Animation):
#     def __init__(
#         self, surface: BesselSurface, start: float, end: float, **kwargs
#     ) -> None:
#         super().__init__(surface, **kwargs)
#         self.start = start
#         self.end = end

#     def interpolate_mobject(self, alpha: float) -> None:
#         time = self.start + (alpha * (self.end - self.start))
#         self.mobject.set_time(time)


class VibratingMembrane(ThreeDScene):
    total_time = 0

    def construct(self):

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        bessel = BesselSurface(3, 1, 2)
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)        
        # bessel.add_updater(lambda surface, dt: surface.set_time(dt))

        self.add(axes, bessel)
        self.wait(3)

        # # self.play(bessel.animate.set_func())
        # self.wait(2)

        # # Play the Count Animation to count from 0 to 100 in 4 seconds
        # self.play(Vibrate(bessel, 0, 5), run_time=3, rate_func=linear)

