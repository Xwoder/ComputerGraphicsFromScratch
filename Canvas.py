from dataclasses import dataclass

from Number import Number
from Vec3 import Vec3


@dataclass
class Canvas:
    width: Number = 800
    height: Number = 600
    pixels: list[list[Vec3]]
