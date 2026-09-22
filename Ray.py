from dataclasses import dataclass

from Point3 import Point3
from Vec3 import Vec3


@dataclass(frozen=True)
class Ray:
    origin: Point3
    direction: Vec3
