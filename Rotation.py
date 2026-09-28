from dataclasses import dataclass

from Number import Number
from geometry.Matrix import Matrix
from geometry.Point3 import Point3


@dataclass(frozen=True)
class Rotation:
    x: Number = 0.0
    y: Number = 0.0
    z: Number = 0.0

    def apply(self, point: Point3) -> Point3:
        """把点按欧拉角旋转（先 X，再 Y，最后 Z），返回旋转后的点。"""
        rotated = Matrix.rotation((self.x, self.y, self.z)).transform(point.to_vec3())
        return Point3(rotated.x, rotated.y, rotated.z)
