from AmbientLight import AmbientLight
from Light import Light
from Number import Number
from Point3 import Point3
from Vec3 import Vec3


class Lighting:
    @staticmethod
    def compute_lighting(
            p: Point3,
            N: Vec3,
            lights: list[Light],
    ) -> Number:

        intensity = 0.0

        for light in lights:

            if isinstance(light, AmbientLight):
                intensity += light.intensity
                continue
            else:
                direction: Vec3 = light.get_direction(p)

                n_dot_l: Number = N @ direction

                if n_dot_l > 0:
                    intensity += (
                            light.intensity
                            * n_dot_l
                            / (N.length() * direction.length())
                    )

        return intensity
