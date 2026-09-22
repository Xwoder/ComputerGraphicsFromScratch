from Number import Number
from Point3 import Point3


class Sphere:
    _center: Point3
    _radius: Number

    def __init__(self, center: Point3, radius: Number):
        """
        初始化球体，使用给定的球心与半径。

        Args:
            center (Point3): 球心坐标（即 Vec3 表示的三维点）。
            radius (Number): 球体半径，取值类型为 float 或 int。
        """

        self._center = center
        self._radius = radius

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

    def __repr__(self) -> str:
        """
        返回球体的官方字符串表示，形如 Sphere(center=..., radius=...)。
        供 repr()、交互式解释器及调试使用。

        Returns:
            str: 包含球心与半径的字符串表示
        """
        return f"Sphere(center={self._center!r}, radius={self._radius})"
