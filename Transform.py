from dataclasses import dataclass

from Number import Number
from Rotation import Rotation
from geometry.Point3 import Point3


@dataclass(frozen=True)
class Transform:
    scale: Number
    rotation: Rotation
    translation: Point3