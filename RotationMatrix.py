from __future__ import annotations

import math
from dataclasses import dataclass

from Matrix import Matrix
from Number import Number


@dataclass(frozen=True)
class RotationMatrix(Matrix):
    """
    旋转矩阵：Matrix 的特化，只表达三维旋转。
    相比通用 Matrix，它提供围绕各坐标轴（X/Y/Z）的便捷构造方法。
    """

    @classmethod
    def around_x(cls, angle: Number) -> RotationMatrix:
        c, s = math.cos(angle), math.sin(angle)
        return cls((
            (1, 0, 0),
            (0, c, -s),
            (0, s, c),
        ))

    @classmethod
    def around_y(cls, angle: Number) -> RotationMatrix:
        c, s = math.cos(angle), math.sin(angle)
        return cls((
            (c, 0, s),
            (0, 1, 0),
            (-s, 0, c),
        ))

    @classmethod
    def around_z(cls, angle: Number) -> RotationMatrix:
        c, s = math.cos(angle), math.sin(angle)
        return cls((
            (c, -s, 0),
            (s,  c, 0),
            (0,  0, 1),
        ))

    @classmethod
    def from_euler(cls, euler: tuple[Number, Number, Number]) -> RotationMatrix:
        """
        由欧拉角（绕 X、Y、Z 轴弧度）组合旋转矩阵。
        组合顺序与 Matrix.rotation 一致：先 X，再 Y，最后 Z。
        """
        rx, ry, rz = euler
        return cls.around_x(rx) @ cls.around_y(ry) @ cls.around_z(rz)
