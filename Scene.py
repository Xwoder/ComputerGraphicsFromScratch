from Color import Color
from Sphere import Sphere


class Scene:
    BACKGROUND_COLOR: Color = Color.Black

    _spheres: list[Sphere]

    def __init__(self, spheres: list[Sphere]):
        self._spheres = spheres

    def add(self, s: Sphere):
        self._spheres.append(s)

    @property
    def spheres(self):
        return self._spheres
