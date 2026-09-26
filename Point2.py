from dataclasses import dataclass

from Number import Number


@dataclass(frozen=True)
class Point2:
    x: Number
    y: Number

    def __sub__(self, other: Point2) -> tuple[Number, Number]:
        """两点相减得到位移向量 (dx, dy)。"""
        return self.x - other.x, self.y - other.y

    def __add__(self, vector: tuple[Number, Number]) -> Point2:
        """加上位移向量 (dx, dy) 得到新点。"""
        return Point2(self.x + vector[0], self.y + vector[1])
