import math

from Color import Color
from Interval import Interval
from Lighting import Lighting
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
            color: Color = closest_sphere.color * Lighting.compute_lighting(point, N,self._scene.lights)
            return color
