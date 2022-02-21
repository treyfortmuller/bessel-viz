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
            surface.become(BesselSurface(BOUNDARY, surrace.orders, surface.modes, timer))

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

class Check(ThreeDScene):
    def construct(self):
        BOUNDARY = 3
        ORDERS = [0, 0]
        MODES = [1, 2]
        timer = 0

        def vibrate(surface: BesselSurface, dt):
            nonlocal timer
            timer += dt
            print(f"{surface.orders}: {timer}")
            surface.become(BesselSurface(BOUNDARY, surface.orders, surface.modes, timer))

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        

        bessel1 = BesselSurface(BOUNDARY, [0], [1], timer)
        bessel1.add_updater(vibrate)

        bessel2 = BesselSurface(BOUNDARY, [1], [1], timer)
        bessel2.add_updater(vibrate)

        surface_group = VGroup(axes, bessel1)
        surface_group.scale(0.8)

        order_and_mode1 = MathTex(f"n={[0]}, m={[1]}", font_size=44)
        order_and_mode1.move_to(np.array([0, -3.0, 0]))
        order_and_mode2 = MathTex(f"n={[1]}, m={[1]}", font_size=44)
        order_and_mode2.move_to(np.array([0, -3.0, 0]))

        # diffyq = MathTex(
        #     r"x^2 \frac{d^2y}{dx^2} + x \frac{dy}{dx} + (x^2 - n^2)y = 0", font_size=56
        # )

        # self.play(Write(diffyq))
        # self.play(diffyq.animate.scale(0.6))
        # self.play(diffyq.animate.to_corner(UL))
        # self.add_fixed_in_frame_mobjects(diffyq)

        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)

        # Start the ambient camera rotation.
        self.begin_ambient_camera_rotation(rate=0.1)

        # Fade in the surface and axes, TODO this isn't fading in the surface...
        self.play(FadeIn(axes), Create(bessel1))

        # This is the janky way to make a mob fixed in frame but not appear
        self.add_fixed_in_frame_mobjects(order_and_mode1)
        self.remove(order_and_mode1)

        # Add the order and mode label to the surface group and render it
        surface_group.add(order_and_mode1)
        self.play(Write(order_and_mode1))

        self.wait(2)

        # remove and create transition
        bessel1.clear_updaters()
        self.remove(bessel1)
        self.play(Transform(order_and_mode1, order_and_mode2), Create(bessel2))

        self.wait(3)

        self.stop_ambient_camera_rotation()