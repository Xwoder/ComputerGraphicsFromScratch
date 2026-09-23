from Sphere import Sphere


class Scene:
    _spheres: list[Sphere]

    def __init__(self, spheres: list[Sphere]):
        self._spheres = spheres

    def add(self, s:Sphere):
        self._spheres.append(s)