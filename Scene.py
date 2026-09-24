from dataclasses import dataclass, field
from typing import ClassVar

from Color import BLACK, Color
from Light import Light
from Sphere import Sphere


@dataclass
class Scene:
    """
    场景：包含物体、光源，以及未命中任何物体时的背景色。
    """

    spheres: list[Sphere] = field(default_factory=list)
    lights: list[Light] = field(default_factory=list)

    BACKGROUND_COLOR: ClassVar[Color] = BLACK
