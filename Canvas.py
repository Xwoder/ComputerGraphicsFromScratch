from Color import Color


class Canvas:
    _width: int = 800
    _height: int = 600
    _pixels: list[list[Color]]
    __defaultColor: Color = Color.Black

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

    def getPixel(self,
                 x: int,
                 y: int) -> Color:
        return self._pixels[y][x]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def defaultColor(self) -> Color:
        return self.__defaultColor
