from pathlib import Path

from Color import Color


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
                    row.append(f"{color.red} {color.green} {color.blue}")
                f.write(" ".join(row) + "\n")
