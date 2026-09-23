from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    """
    RGB 颜色，每个分量取值 0~255。
    """

    red: int
    green: int
    blue: int


BLACK: Color = Color(0, 0, 0)
WHITE: Color = Color(255, 255, 255)
