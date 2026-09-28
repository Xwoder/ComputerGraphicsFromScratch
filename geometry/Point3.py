from dataclasses import dataclass
from typing import overload

from Number import Number
from geometry.Vec3 import Vec3


@dataclass(frozen=True)
class Point3:
    x: Number
    y: Number
    z: Number

    @overload
    def __sub__(self, other: Point3) -> Vec3:
        ...

    @overload
    def __sub__(self, other: Vec3) -> Point3:
        ...

    def __sub__(self, other: Point3 | Vec3) -> Point3 | Vec3:
        if isinstance(other, Point3):
            return Vec3(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
            )

        if isinstance(other, Vec3):
            return Point3(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
            )

        return NotImplemented

    def __add__(self, vector: Vec3) -> Point3:
        return Point3(
            self.x + vector.x,
            self.y + vector.y,
            self.z + vector.z,
        )

    def __mul__(self, scalar: Number) -> Point3:
        """
        标量乘法（p * t），各分量乘以标量 t，返回新点（相对原点缩放）。
        不修改原点。标量必须写在右侧。
        """
        return Point3(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )

    def __rmul__(self, scalar: Number) -> Point3:
        """
        右乘（t * p），使标量可写在左侧，直接复用 __mul__。
        """
        return self.__mul__(scalar)

    def to_vec3(self) -> Vec3:
        """把点当作从原点出发的位置向量，转换为 Vec3。"""
        return Vec3(self.x, self.y, self.z)
