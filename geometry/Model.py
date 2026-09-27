from dataclasses import dataclass

from Rasterizer import Triangle
from color.Color import Color
from geometry.Point3 import Point3


@dataclass
class Model:
    name: str
    vertices: list[Point3]
    triangles: list[Triangle]

    @staticmethod
    def create_cube() -> Model:
        vertices = [
            Point3(1, 1, 1),
            Point3(-1, 1, 1),
            Point3(-1, -1, 1),
            Point3(1, -1, 1),
            Point3(1, 1, -1),
            Point3(-1, 1, -1),
            Point3(-1, -1, -1),
            Point3(1, -1, -1),
        ]

        triangles = [
            Triangle((0, 1, 2), Color.RED),
            Triangle((0, 2, 3), Color.RED),
            Triangle((4, 0, 3), Color.GREEN),
            Triangle((4, 3, 7), Color.GREEN),
            Triangle((5, 4, 7), Color.BLUE),
            Triangle((5, 7, 6), Color.BLUE),
            Triangle((1, 5, 6), Color.YELLOW),
            Triangle((1, 6, 2), Color.YELLOW),
            Triangle((4, 5, 1), Color.PURPLE),
            Triangle((4, 1, 0), Color.PURPLE),
            Triangle((2, 6, 7), Color.CYAN),
            Triangle((2, 7, 3), Color.CYAN),
        ]

        return Model(
            name="cube",
            vertices=vertices,
            triangles=triangles,
        )
