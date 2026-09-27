from dataclasses import dataclass

from geometry.Triangle import Triangle
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
            Triangle(0, (0, 1, 2), Color.RED),
            Triangle(1, (0, 2, 3), Color.RED),
            Triangle(2, (4, 0, 3), Color.GREEN),
            Triangle(3, (4, 3, 7), Color.GREEN),
            Triangle(4, (5, 4, 7), Color.BLUE),
            Triangle(5, (5, 7, 6), Color.BLUE),
            Triangle(6, (1, 5, 6), Color.YELLOW),
            Triangle(7, (1, 6, 2), Color.YELLOW),
            Triangle(8, (4, 5, 1), Color.PURPLE),
            Triangle(9, (4, 1, 0), Color.PURPLE),
            Triangle(10, (2, 6, 7), Color.CYAN),
            Triangle(11, (2, 7, 3), Color.CYAN),
        ]

        return Model(
            name="cube",
            vertices=vertices,
            triangles=triangles,
        )
