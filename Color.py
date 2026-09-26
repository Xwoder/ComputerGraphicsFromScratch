from dataclasses import dataclass
from typing import ClassVar

from Number import Number


@dataclass(frozen=True)
class Color:
    """
    RGB 颜色，每个分量取值 0~255。
    """

    red: int
    green: int
    blue: int

    BLACK: ClassVar["Color"]
    WHITE: ClassVar["Color"]
    RED: ClassVar["Color"]
    GREEN: ClassVar["Color"]
    BLUE: ClassVar["Color"]

    def __mul__(self, number: Number) -> Color:
        return Color(
            max(0, min(int(self.red * number), 255)),
            max(0, min(int(self.green * number), 255)),
            max(0, min(int(self.blue * number), 255)),
        )

    def __add__(self, other: Color) -> Color:
        return Color(
            min(self.red + other.red, 255),
            min(self.green + other.green, 255),
            min(self.blue + other.blue, 255),
        )


Color.BLACK = Color(0, 0, 0)
Color.WHITE = Color(255, 255, 255)
Color.RED = Color(255, 0, 0)
Color.GREEN = Color(0, 255, 0)
Color.BLUE = Color(0, 0, 255)
