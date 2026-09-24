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
        """
        颜色按标量缩放（乘以光照强度）：各分量先乘后截断到 0~255。

        镜面高光会让总强度超过 1，若不截断会写出非法的 PPM 分量值。
        """

        return Color(
            min(int(self.red * number), 255),
            min(int(self.green * number), 255),
            min(int(self.blue * number), 255),
        )


BLACK: Color = Color(0, 0, 0)
WHITE: Color = Color(255, 255, 255)
