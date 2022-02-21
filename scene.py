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

        def create_bessel(scene, orders, modes):
            bessel = BesselSurface(BOUNDARY, orders, modes, timer)
            bessel.add_updater(vibrate)
            label = MathTex(f"n={orders}, m={modes}", font_size=44)
            scene.add_fixed_in_frame_mobjects(label)
            scene.remove(label)
            label.move_to(np.array([0, -3.0, 0]))
            return bessel, label

        def transition(scene, outgoing_bessel, outgoing_label, incoming_bessel, incoming_label):
            outgoing_bessel.clear_updaters()
            scene.remove(outgoing_bessel)
            scene.play(Transform(outgoing_label, incoming_label), Create(incoming_bessel))


        def vibrate(surface: BesselSurface, dt):
            nonlocal timer
            timer += dt
            surface.become(BesselSurface(BOUNDARY, surface.orders, surface.modes, timer))

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        
        b1, l1 = create_bessel(self, [0], [1])
        b2, l2 = create_bessel(self, [1], [1])
        b3, l3 = create_bessel(self, [3], [2])
        b4, l4 = create_bessel(self, [4], [5])
        b5, l5 = create_bessel(self, [0, 1, 2, 3, 4], [1, 2, 3, 4, 5])

        surface_group = VGroup(axes, b1)
        surface_group.scale(0.8)

        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Fade in the surface and axes, TODO this isn't fading in the surface...
        self.play(FadeIn(axes), Create(b1))
        self.wait(1)
        self.play(Write(l1))
        self.wait(3)
        
        transition(self, b1, l1, b2, l2)
        self.wait(3)
        transition(self, b2, l2, b3, l3)
        self.wait(3)
        transition(self, b3, l3, b4, l4)
        self.wait(3)
        transition(self, b4, l4, b5, l5)
        self.wait(3)

        self.stop_ambient_camera_rotation()