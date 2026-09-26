import math
from dataclasses import dataclass, field

from Color import Color
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

    BACKGROUND_COLOR: Color = Color.BLACK

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

        closest_t: Number = math.inf  # 当前最近命中距离，初始化为正无穷表示尚未命中
        closest_sphere: Sphere | None = None  # 最近命中的球体，初始化为 None 表示未命中

        for sphere in self.spheres:  # 遍历场景中的每一个球体
            t1, t2 = sphere.intersect(ray)  # 求射线与该球体的两个解析交点参数 t

            for t in (t1, t2):  # 依次检查两个根
                if t in interval and t < closest_t:  # 根必须在有效区间内，且比当前最近距离更近
                    closest_t = t  # 更新最近命中距离
                    closest_sphere = sphere  # 记录对应的球体

        return closest_sphere, closest_t  # 返回最近命中的球体与 t；未命中时为 (None, inf)
