from dataclasses import dataclass

from Number import Number


@dataclass(frozen=True)
class Color:
    """
    RGB 颜色，每个分量取值 0~255。
    """

    red: int
    green: int
    blue: int

    def __mul__(self, number: Number) -> Color:
        return Color(
            int(self.red * number),
            int(self.green * number),
            int(self.blue * number),
        )


BLACK: Color = Color(0, 0, 0)
WHITE: Color = Color(255, 255, 255)
