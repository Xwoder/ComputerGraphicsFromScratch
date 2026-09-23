import math

from Color import Color
from Interval import Interval
from Ray import Ray
from Scene import Scene
from Sphere import Sphere


class RayTracer:
    _scene: Scene

    def __init__(self, scene: Scene):
        self._scene = scene

    def traceRay(
            self,
            ray: Ray,
            interval: Interval,
    ) -> Color:
        closest_t = +math.inf
        closest_sphere: Sphere | None = None

        for sphere in self._scene.spheres:
            for t in sphere.intersect(ray):
                if t in interval and t < closest_t:
                    closest_t, closest_sphere = t, sphere

        if closest_sphere is not None:
            return closest_sphere.color
        else:
            return self._scene.BACKGROUND_COLOR
