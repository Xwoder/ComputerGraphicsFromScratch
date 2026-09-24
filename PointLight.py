from dataclasses import dataclass

from Light import Light
from Point3 import Point3
from Vec3 import Vec3

@dataclass
class PointLight(Light):
    position: Point3

    def get_direction(self, p: Point3) -> Vec3:
        return self.position - p
