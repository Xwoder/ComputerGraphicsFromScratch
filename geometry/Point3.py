from dataclasses import dataclass
from typing import overload

from Number import Number
from Vec3 import Vec3


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
