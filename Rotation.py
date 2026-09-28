from dataclasses import dataclass

from Number import Number


@dataclass(frozen=True)
class Rotation:
    x: Number = 0.0
    y: Number = 0.0
    z: Number = 0.0
