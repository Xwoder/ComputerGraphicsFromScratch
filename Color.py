class Color:
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


Color.Black: Color = Color(0, 0, 0)
Color.White: Color = Color(255, 255, 255)
