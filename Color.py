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


Color.Black = Color(0, 0, 0)
Color.White = Color(255, 255, 255)
