from manim import *
from functools import partial
from scipy import special


class BesselSurface(Surface):
    def __init__(
        self, boundary: float, orders: List[int], modes: List[int], time: float
    ):
        self.boundary = boundary
        self.orders = orders
        self.modes = modes
        self.time = time

        super().__init__(self.func, u_range=[0, self.boundary], v_range=[0, 2 * PI])

    @staticmethod
    def modal_freq(boundary, order, mode):
        # grab the zero for the mode and order that we care about
        zero = special.jn_zeros(order, mode)[mode - 1]
        return zero / boundary

    def func(self, u, v):
        r, phi, z = u, v, 0

        for i in range(0, len(self.orders)):
            n = self.orders[i]
            m = self.modes[i]

            omega = BesselSurface.modal_freq(self.boundary, n, m)

            z += special.jv(n, omega * r) * np.cos(n * phi) * np.cos(omega * self.time)

        z /= len(self.orders)

        return np.array([r * np.cos(phi), r * np.sin(phi), z])


class ComboBesselScene(ThreeDScene):
    def construct(self):
        BOUNDARY = 3
        ORDERS = [0, 0]
        MODES = [1, 2]
        timer = 0

        def vibrate(surface: BesselSurface, dt):
            nonlocal timer
            timer += dt
            surface.become(BesselSurface(BOUNDARY, ORDERS, MODES, timer))

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        bessel = BesselSurface(BOUNDARY, ORDERS, MODES, timer)
        bessel.add_updater(vibrate)

        surface_group = VGroup(axes, bessel)
        surface_group.scale(0.8)

        diffyq = MathTex(
            r"x^2 \frac{d^2y}{dx^2} + x \frac{dy}{dx} + (x^2 - n^2)y = 0", font_size=56
        )
        order_and_mode = MathTex(f"n={ORDERS}, m={MODES}", font_size=44)

        self.play(Write(diffyq))
        self.play(diffyq.animate.scale(0.6))
        self.play(diffyq.animate.to_corner(UL))
        self.add_fixed_in_frame_mobjects(diffyq)

        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)

        # Start the ambient camera rotation.
        self.begin_ambient_camera_rotation(rate=0.1)

        # Fade in the surface and axes, TODO this isn't fading in the surface...
        self.play(FadeIn(axes), Create(bessel))

        # This is the janky way to make a mob fixed in frame but not appear
        self.add_fixed_in_frame_mobjects(order_and_mode)
        self.remove(order_and_mode)

        # Add the order and mode label to the surface group and render it
        surface_group.add(order_and_mode)
        self.play(Write(order_and_mode.move_to(np.array([0, -3.0, 0]))))

        self.wait(5)
        self.stop_ambient_camera_rotation()


class BesselGrid(ThreeDScene):
    def construct(self):
        BOUNDARY = 3
        ORDERS = [0, 0]
        MODES = [1, 2]
        timer = 0

        def vibrate(surface: BesselSurface, dt):
            nonlocal timer
            timer += dt
            surface.become(BesselSurface(BOUNDARY, ORDERS, MODES, timer))

        axes1 = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        axes2 = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        axes3 = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        axes4 = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        bessel1 = BesselSurface(BOUNDARY, [0], [1], timer)
        bessel2 = BesselSurface(BOUNDARY, [1], [1], timer)
        bessel3 = BesselSurface(BOUNDARY, [2], [1], timer)
        bessel4 = BesselSurface(BOUNDARY, [3], [1], timer)

        # bessel1.add_updater(vibrate)
        # bessel2.add_updater(vibrate)

        surface_group1 = VGroup(axes1, bessel1)
        surface_group1.scale(0.3)
        surface_group1.move_to(2 * UL)

        surface_group2 = VGroup(axes2, bessel2)
        surface_group2.scale(0.3)
        surface_group2.move_to(2 * UR)

        surface_group3 = VGroup(axes3, bessel3)
        surface_group3.scale(0.3)
        surface_group3.move_to(2 * DL)

        surface_group4 = VGroup(axes4, bessel4)
        surface_group4.scale(0.3)
        surface_group4.move_to(2 * DR)

        self.set_camera_orientation(theta=90 * DEGREES, phi=70 * DEGREES)

        # Start the ambient camera rotation.
        # self.begin_ambient_camera_rotation(rate=0.1)

        # Fade in the surface and axes, TODO this isn't fading in the surface...
        # self.play(FadeIn(axes), Create(bessel))

        self.add(surface_group1, surface_group2, surface_group3, surface_group4)
        self.play(
            Rotate(surface_group1, PI/4, np.array([0, 0, 1]), run_time=2),
            Rotate(surface_group2, -PI/4, np.array([0, 0, 1]), run_time=2),
            Rotate(surface_group3, -PI/4, np.array([0, 0, 1]), run_time=2),
            Rotate(surface_group4, -PI/4, np.array([0, 0, 1]), run_time=2),
        )

        # self.wait(3)
        # self.stop_ambient_camera_rotation()

        # TODO box grid example
        # boxes=VGroup(*[Square() for s in range(0,6)])
        # boxes.arrange_in_grid(rows=2, buff=1)
        # self.add(boxes)

        # surfaces = VGroup(*[surface_group for s in range(0, 6)])
        # surfaces.arrange_in_grid(rows=2, buff=1)
        # self.add(surfaces)
