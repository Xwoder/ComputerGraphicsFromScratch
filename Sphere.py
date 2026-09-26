import math

from dataclasses import dataclass, field

from Color import  Color
from Number import Number
from Point3 import Point3
from Ray import Ray


@dataclass(frozen=True)
class Sphere:
    """
    球体：由球心、半径、表面颜色、高光指数与反射率定义。
    """

    center: Point3
    radius: Number
    color: Color = Color.WHITE
    specular: Number = 0
    reflective: Number = 0
    # 半径平方，构造时预计算，避免每次求交重复 self.radius ** 2。
    radius_squared: Number = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "radius_squared", self.radius ** 2)

    def intersect(self, ray: Ray) -> tuple[float, float]:
        """
        求射线与球体的交点参数（ray-tracing 的解析求根）。

        将射线 P(t) = origin + t * direction 代入球面方程
        |P - center|² = radius²，得到关于 t 的一元二次方程：

            a = D·D
            b = 2 * OC·D          （用 half_b = OC·D 简化）
            c = OC·OC - radius²
            discriminant = half_b² - a*c

        其中 OC = origin - center。判别式小于 0 表示无实根（未命中）。

        Args:
            ray (Ray): 待求交的射线（direction 不必是单位向量）。

        Returns:
            tuple[float, float]: (t1, t2)，满足 t1 <= t2 的两个交点参数；
            未命中时返回 (inf, inf)，便于调用方直接用 `t in interval` 过滤。
        """

        oc = ray.origin - self.center
        a: Number = ray.direction @ ray.direction
        half_b: Number = oc @ ray.direction
        c: Number = oc @ oc - self.radius_squared

        discriminant: Number = half_b * half_b - a * c

        if discriminant < 0:
            return math.inf, math.inf
        else:
            sqrt_disc: Number = math.sqrt(discriminant)
            t1: Number = (-half_b - sqrt_disc) / a
            t2: Number = (-half_b + sqrt_disc) / a

            return t1, t2
