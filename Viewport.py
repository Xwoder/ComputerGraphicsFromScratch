from dataclasses import dataclass

from Number import Number


@dataclass
class Viewport:
    width: Number = 1
    height: Number = 1
    distance: Number = 1
