from dataclasses import dataclass

from color.Color import Color


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
