import math

from Light.AmbientLight import AmbientLight
from Color import Color
from Interval import Interval
from Light import Light
from Number import Number
from Point3 import Point3
from Ray import Ray
from Scene import Scene
from Vec3 import Vec3


class RayTracer:
    _scene: Scene

    def __init__(self, scene: Scene):
        self._scene = scene

    def traceRay(self, ray: Ray) -> Color:
        closest_t = math.inf
        closest_sphere = None

        for sphere in self._scene.spheres:
            for t in sphere.intersect(ray):
                if t in Interval(1, math.inf) and t < closest_t:
                    closest_t = t
                    closest_sphere = sphere

        if closest_sphere is None:
            return self._scene.BACKGROUND_COLOR
        else:
            point: Point3 = ray.at(closest_t)
            N: Vec3 = (point - closest_sphere.center).normalize()
            color: Color = closest_sphere.color * self.compute_lighting(point, N, self._scene.lights)
            return color

    @staticmethod
    def compute_lighting(
            p: Point3,
            N: Vec3,
            lights: list[Light],
    ) -> Number:

        # N 由调用方保证已归一化（traceRay），分母中的 |N| 恒为 1，无需再除。
        # 每个光源只需把光方向归一化一次，即可直接用点积得到 cos(theta)。
        intensity = 0.0

        for light in lights:

            if isinstance(light, AmbientLight):
                intensity += light.intensity
                continue
            else:
                direction: Vec3 = light.get_direction(p)

                # 退化情形：点光源恰好落在着色点上，方向为零向量，无法归一化
                if direction.length_squared() == 0:
                    continue

                L: Vec3 = direction.normalize()

                n_dot_l: Number = N.dot(L)

                if n_dot_l > 0:
                    intensity += light.intensity * n_dot_l

        return intensity
