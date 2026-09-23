from dataclasses import dataclass
from typing import ClassVar

from Color import BLACK, Color
from Sphere import Sphere


@dataclass
class Scene:
    """
    场景：包含一组球体，以及未命中任何球体时的背景色。
    """

    spheres: list[Sphere]
    BACKGROUND_COLOR: ClassVar[Color] = BLACK

    def add(self, s: Sphere) -> None:
        self.spheres.append(s)
