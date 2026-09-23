class Color:
    # 先在类体内声明（仅注解，不赋值），类创建后再赋值，静态检查器才能解析 Color.Black / Color.White
    Black: Color
    White: Color

    _red: int
    _green: int
    _blue: int

    def __init__(self,
                 red: int,
                 green: int,
                 blue: int) -> None:
        super().__init__()

        self._red = red
        self._green = green
        self._blue = blue

    @property
    def red(self) -> int:
        """
        红色分量（只读属性）。

        Returns:
            int: 红色分量，取值 0~255
        """
        return self._red

    @property
    def green(self) -> int:
        """
        绿色分量（只读属性）。

        Returns:
            int: 绿色分量，取值 0~255
        """
        return self._green

    @property
    def blue(self) -> int:
        """
        蓝色分量（只读属性）。

        Returns:
            int: 蓝色分量，取值 0~255
        """
        return self._blue

    def __repr__(self) -> str:
        return f"Color({self._red}, {self._green}, {self._blue})"


Color.Black = Color(0, 0, 0)
Color.White = Color(255, 255, 255)
