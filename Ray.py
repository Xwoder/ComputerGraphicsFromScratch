from dataclasses import dataclass

from Number import Number
from Point3 import Point3
from Vec3 import Vec3


@dataclass(frozen=True)
class Ray:
    origin: Point3
    direction: Vec3

    def at(self, t: Number) -> Point3:
        return self.origin + t * self.direction
