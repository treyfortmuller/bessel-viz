from manim import *
from functools import partial
from scipy import special


class BesselSurface(Surface):
    def __init__(self, boundary, order, mode, time):
        self.boundary = boundary
        self.order = order
        self.mode = mode
        self.time = time

        super().__init__(self.func, u_range=[0, self.boundary], v_range=[0, 2 * PI])

    def modal_freq(self):
        # grab the zero for the mode and order that we care about
        zero = special.jn_zeros(self.order, self.mode)[self.mode - 1]
        return zero / self.boundary

    def func(self, u, v):
        r, phi = u, v
        z = (
            special.jv(self.order, self.modal_freq() * r)
            * np.cos(self.order * phi)
            * np.cos(self.modal_freq() * self.time)
        )
        return np.array([r * np.cos(phi), r * np.sin(phi), z])


class BesselScene(ThreeDScene):
    def construct(self):
        BOUNDARY = 3
        ORDER = 5
        MODE = 4
        timer = 0

        def vibrate(surface: BesselSurface, dt):
            nonlocal timer
            timer += dt
            surface.become(BesselSurface(BOUNDARY, ORDER, MODE, timer))

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        bessel = BesselSurface(BOUNDARY, ORDER, MODE, timer)
        bessel.add_updater(vibrate)

        surface_group = VGroup(axes, bessel)
        surface_group.scale(0.8)

        diffyq = MathTex(
            r"x^2 \frac{d^2y}{dx^2} + x \frac{dy}{dx} + (x^2 - n^2)y = 0", font_size=56
        )
        order_and_mode = MathTex(f"n={ORDER}, m={MODE}", font_size=44)

        self.play(Write(diffyq))
        self.play(diffyq.animate.scale(0.6))
        self.play(diffyq.animate.to_corner(UL))
        self.add_fixed_in_frame_mobjects(diffyq)

        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)

        self.begin_ambient_camera_rotation(rate=0.1)
        # self.add(surface_group)

        self.play(FadeIn(axes, bessel))

        # self.add_fixed_in_frame_mobjects(order_and_mode.align_to(surface_group, DOWN))
        self.add_fixed_in_frame_mobjects(order_and_mode)
        self.remove(order_and_mode)
        # self.play(Write(order_and_mode.align_to(surface_group, DOWN)))

        # VGroup(surface_group, order_and_mode).arrange(DOWN)
        self.play(Write(order_and_mode.move_to(np.array([0, -3.0, 0]))))

        self.wait(2)
        self.stop_ambient_camera_rotation()

        # align_to(mobject_or_point, direction=array([0., -1., 0.]), alignment_vect=array([0., 1., 0.]))
