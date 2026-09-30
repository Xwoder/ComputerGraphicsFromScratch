from pathlib import Path

from PIL import Image
from color.Color import Color
from geometry.Point2 import Point2


class Canvas:
    _width: int = 800
    _height: int = 600
    _pixels: list[list[Color]]
    __defaultColor: Color = Color.WHITE

    def __init__(self,
                 width: int,
                 height: int) -> None:
        super().__init__()

        self._width = width
        self._height = height
        self._pixels = [[self.__defaultColor for _ in range(width)]
                        for _ in range(height)]

    def putPixel(self,
                 x: int,
                 y: int,
                 color: Color) -> None:
        self._pixels[y][x] = color

    def drawLine(self,
                 startPoint: Point2,
                 endPoint: Point2,
                 color: Color) -> None:
        """
        Bresenham 整数直线栅格化：用 color 点亮 p0→p1 经过的所有栅格单元。

        p0 / p1 是带坐标 (x, y) 的点（如 Camera.projectVertex 返回的 Point2，
        坐标可能为小数），这里先 round 吸附到最近栅格，再按标准 Bresenham
        同时处理 x 主轴与 y 主轴两种情况。
        """
        x0: int = round(startPoint.x)
        y0: int = round(startPoint.y)
        x1: int = round(endPoint.x)
        y1: int = round(endPoint.y)

        dx: int = abs(x1 - x0)
        dy: int = abs(y1 - y0)
        sx: int = 1 if x0 < x1 else -1
        sy: int = 1 if y0 < y1 else -1
        err: int = dx - dy

        while True:
            self.putPixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2: int = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def savePPM(self, path: Path) -> None:
        """
        把画布内容写成纯文本 PPM（P3）文件。

        文件结构为：魔数 "P3"、宽高、最大分量值 255，随后是行优先排列的
        十进制 RGB 三元组（空格分隔，一像素一行对应画布的一行）。
        纯 ASCII 文本，可直接用文本编辑器查看，无需任何第三方依赖。

        Args:
            path (Path): 输出文件路径。
        """

        # 确保输出文件所在的目录存在（如默认 output/ 文件夹）。
        path.parent.mkdir(parents=True, exist_ok=True)

        # 逐行构造并写入：每行像素拼成单个字符串后立即写出，不缓存整图，
        # 把峰值内存从「整张图的大字符串」降到「单行」，对 480k 像素更友好。
        with open(path, "w", encoding="ascii") as f:
            f.write("P3\n")
            f.write(f"{self._width} {self._height}\n")
            f.write("255\n")
            for y in range(self._height):
                row = []
                for x in range(self._width):
                    color = self._pixels[y][x]
                    row.append(" ".join(map(str, color.as_tuple())))
                f.write(" ".join(row) + "\n")

    def savePNG(self, path: Path) -> None:
        """
        把画布内容写成 PNG 文件（借助 Pillow）。

        像素逐行（行优先，y 外层、x 内层）从 ``_pixels`` 取出，转换为
        ``(R, G, B)`` 整数三元组后交给 Pillow 写出。颜色取值与 ``savePPM``
        完全一致（0–255），            仅编码格式不同。

        Args:
            path (Path): 输出文件路径（通常以 ``.png`` 结尾）。
        """
        # 确保输出文件所在的目录存在（如默认 output/ 文件夹）。
        path.parent.mkdir(parents=True, exist_ok=True)

        img = Image.new("RGB", (self._width, self._height))
        pixels = [
            self._pixels[y][x].as_tuple()
            for y in range(self._height)
            for x in range(self._width)
        ]
        img.putdata(pixels)
        img.save(path)
