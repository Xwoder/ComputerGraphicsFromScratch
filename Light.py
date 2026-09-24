from dataclasses import dataclass

from Number import Number
from Point3 import Point3
from Vec3 import Vec3


@dataclass
class Light:
    intensity: Number

    def get_direction(self, p: Point3) -> Vec3:
        raise NotImplementedError