from dataclasses import dataclass
from typing import override

from light.Light import Light
from geometry.Point3 import Point3
from geometry.Vec3 import Vec3


@dataclass
class DirectionalLight(Light):
    direction: Vec3

    @override
    def get_direction(self, p: Point3) -> Vec3:
        return self.direction