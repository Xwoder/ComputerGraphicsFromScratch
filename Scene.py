import math
from dataclasses import dataclass, field

from Color import Color, WHITE
from Interval import Interval
from Light.Light import Light
from Number import Number
from Ray import Ray
from Sphere import Sphere


@dataclass
class Scene:
    """
    场景：包含物体、光源，以及未命中任何物体时的背景色。
    """

    spheres: list[Sphere] = field(default_factory=list)
    lights: list[Light] = field(default_factory=list)

    BACKGROUND_COLOR: Color = WHITE

    def closestIntersection(self, ray: Ray, interval: Interval) -> tuple[Sphere | None, Number]:
        closest_t = math.inf
        closest_sphere = None

        for sphere in self.spheres:
            t1, t2 = sphere.intersect(ray)

            if interval.min <= t1 <= Interval.max and t1 < closest_t:
                closest_t = t1
                closest_sphere = sphere

            if interval.min <= t2 <= interval.max and t2 < closest_t:
                closest_t = t2
                closest_sphere = sphere

        return closest_sphere, closest_t
