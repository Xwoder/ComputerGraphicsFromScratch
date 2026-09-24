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
        """
        求射线在给定区间内与场景的最近交点。

        遍历全部球体，逐一取其解析解 (t1, t2)，只接受落在 `interval` 内的根，
        并保留最小者作为最近命中。返回 (球体, t) 二元组，未命中时球体为 None。

        Args:
            ray (Ray): 待求交的射线。
            interval (Interval): 有效 `t` 区间，例如 Interval(1, inf) 表示视口前方的命中。

        Returns:
            tuple[Sphere | None, Number]: (最近命中的球体, 对应的 t)；未命中时为 (None, inf)。
        """

        closest_t: Number = math.inf
        closest_sphere: Sphere | None = None

        for sphere in self.spheres:
            t1, t2 = sphere.intersect(ray)

            for t in (t1, t2):
                if t in interval and t < closest_t:
                    closest_t = t
                    closest_sphere = sphere

        return closest_sphere, closest_t
