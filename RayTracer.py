import math

from Color import Color
from Interval import Interval
from Ray import Ray
from Scene import Scene


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
            return closest_sphere.color
