import math

from Color import Color
from Number import Number
from Point3 import Point3
from Ray import Ray


class Sphere:
    _center: Point3
    _radius: Number
    _color: Color

    def __init__(self,
                 center: Point3,
                 radius: Number,
                 color: Color = Color.White):
        """
        初始化球体，使用给定的球心、半径与颜色。

        Args:
            center (Point3): 球心坐标（即 Vec3 表示的三维点）。
            radius (Number): 球体半径，取值类型为 float 或 int。
            color (Color): 球体表面颜色，默认白色。
        """

        self._center = center
        self._radius = radius
        self._color = color

    @property
    def center(self) -> Point3:
        """
        球心（只读属性）。

        Returns:
            Point3: 球心所在的三维点
        """
        return self._center

    @property
    def radius(self) -> Number:
        """
        半径（只读属性）。

        Returns:
            Number: 球体半径
        """
        return self._radius

    @property
    def color(self) -> Color:
        """
        颜色（只读属性）。

        Returns:
            Color: 球体表面颜色
        """
        return self._color

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

        oc = ray.origin - self._center
        a: Number = ray.direction.dot(ray.direction)
        half_b: Number = oc.dot(ray.direction)
        c: Number = oc.dot(oc) - self._radius ** 2

        discriminant: Number = half_b * half_b - a * c

        if discriminant < 0:
            return math.inf, math.inf
        else:
            sqrt_disc: Number = math.sqrt(discriminant)
            t1: Number = (-half_b - sqrt_disc) / a
            t2: Number = (-half_b + sqrt_disc) / a

            return t1, t2

    def __repr__(self) -> str:
        """
        返回球体的官方字符串表示，形如 Sphere(center=..., radius=..., color=...)。
        供 repr()、交互式解释器及调试使用。

        Returns:
            str: 包含球心、半径与颜色的字符串表示
        """
        return (f"Sphere(center={self._center!r}, "
                f"radius={self._radius}, "
                f"color={self._color!r})")
