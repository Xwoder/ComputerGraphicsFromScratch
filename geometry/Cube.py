from dataclasses import dataclass, field

from color.Color import Color
from geometry.Point3 import Point3


@dataclass(frozen=True)
class Triangle:
    """一个三角形面片。

    - id: 三角形编号（如 0, 1, 2, ...）。
    - vertex_indices: 它关联的三个顶点编号（如 (0, 1, 2)，可缩写为 "012"）。
    - color: 该三角形的颜色。
    """

    id: int
    vertex_indices: tuple[int, int, int]
    color: Color

    @property
    def vertices(self) -> tuple[int, int, int]:
        """关联顶点的编号列表。"""
        return self.vertex_indices

    def indices_code(self) -> str:
        """以紧凑形式返回编号，如 (0, 1, 2) -> "012"，方便作为键或显示。"""
        return "".join(str(i) for i in self.vertex_indices)


@dataclass
class Cube:
    """立方体，由顶点字典与三角形字典构成。

    - vertices: 顶点编号 -> 坐标 (Point3)。
    - triangles: 三角形编号 -> Triangle 对象。
    """

    vertices: dict[int, Point3] = field(default_factory=dict)
    triangles: dict[int, Triangle] = field(default_factory=dict)

    @classmethod
    def unit_cube(cls) -> Cube:
        """构造一个边长为 2、中心在原点的单位立方体（带彩色面片）。"""
        vertices: dict[int, Point3] = {
            0: Point3(1, 1, 1),
            1: Point3(-1, 1, 1),
            2: Point3(-1, -1, 1),
            3: Point3(1, -1, 1),
            4: Point3(1, 1, -1),
            5: Point3(-1, 1, -1),
            6: Point3(-1, -1, -1),
            7: Point3(1, -1, -1),
        }

        triangles: dict[int, Triangle] = {
            0: Triangle(0, (0, 1, 2), Color.RED),
            1: Triangle(1, (0, 2, 3), Color.RED),
            2: Triangle(2, (4, 0, 3), Color.GREEN),
            3: Triangle(3, (4, 3, 7), Color.GREEN),
            4: Triangle(4, (5, 4, 7), Color.BLUE),
            5: Triangle(5, (5, 7, 6), Color.BLUE),
            6: Triangle(6, (1, 5, 6), Color.YELLOW),
            7: Triangle(7, (1, 6, 2), Color.YELLOW),
            8: Triangle(8, (4, 5, 1), Color.PURPLE),
            9: Triangle(9, (4, 1, 0), Color.PURPLE),
            10: Triangle(10, (2, 6, 7), Color.CYAN),
            11: Triangle(11, (2, 7, 3), Color.CYAN),
        }

        return cls(vertices=vertices, triangles=triangles)
