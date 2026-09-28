from __future__ import annotations

from dataclasses import dataclass

from Number import Number
from geometry.Point3 import Point3
from geometry.Matrix import Matrix


@dataclass(frozen=True)
class Matrix4:
    """4×4 齐次矩阵，用于光栅化管线的仿射变换合成。

    与仅支持 3×3 旋转的 Matrix 不同，Matrix4 同时容纳缩放、旋转与平移，
    因而可以把「相机变换 × 实例变换」合成为单一矩阵，再一次性作用到顶点上，
    对应 RenderScene / RenderModel 伪代码里的 transform * V 与 M_camera * I.transform。
    """

    rows: tuple[tuple[Number, ...], ...]

    def __post_init__(self) -> None:
        if len(self.rows) != 4 or any(len(row) != 4 for row in self.rows):
            raise ValueError("Matrix4 must be a 4x4 matrix.")

    @staticmethod
    def identity() -> Matrix4:
        return Matrix4((
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 1),
        ))

    @staticmethod
    def translation(x: Number, y: Number, z: Number) -> Matrix4:
        return Matrix4((
            (1, 0, 0, x),
            (0, 1, 0, y),
            (0, 0, 1, z),
            (0, 0, 0, 1),
        ))

    @staticmethod
    def scaling(s: Number) -> Matrix4:
        return Matrix4((
            (s, 0, 0, 0),
            (0, s, 0, 0),
            (0, 0, s, 0),
            (0, 0, 0, 1),
        ))

    @staticmethod
    def rotation(euler: tuple[Number, Number, Number]) -> Matrix4:
        """由欧拉角（先 X、再 Y、最后 Z）构造 4×4 旋转矩阵。"""
        return Matrix4.from_matrix3(Matrix.rotation(euler))

    @staticmethod
    def from_matrix3(m: Matrix) -> Matrix4:
        """把 3×3 旋转矩阵嵌入到 4×4 齐次矩阵的左上角。"""
        return Matrix4((
            (m[0][0], m[0][1], m[0][2], 0),
            (m[1][0], m[1][1], m[1][2], 0),
            (m[2][0], m[2][1], m[2][2], 0),
            (0, 0, 0, 1),
        ))

    def __matmul__(self, other: Matrix4) -> Matrix4:
        """矩阵乘法（self · other），要求 self 列数 == other 行数（此处恒为 4）。"""
        if len(self.rows[0]) != len(other.rows):
            raise ValueError("Matrix4 dimensions are incompatible for multiplication.")

        result = tuple(
            tuple(
                sum(self.rows[i][k] * other.rows[k][j] for k in range(4))
                for j in range(4)
            )
            for i in range(4)
        )
        return Matrix4(result)

    def transform_point(self, p: Point3) -> Point3:
        """把 3D 点当作齐次坐标 (x, y, z, 1) 左乘本矩阵，返回变换后的点。

        仿射矩阵最后一行恒为 (0, 0, 0, 1)，故 w 必为 1；此处仍做通用齐次除法以兼容投影矩阵。
        """
        x = self.rows[0][0] * p.x + self.rows[0][1] * p.y + self.rows[0][2] * p.z + self.rows[0][3]
        y = self.rows[1][0] * p.x + self.rows[1][1] * p.y + self.rows[1][2] * p.z + self.rows[1][3]
        z = self.rows[2][0] * p.x + self.rows[2][1] * p.y + self.rows[2][2] * p.z + self.rows[2][3]
        w = self.rows[3][0] * p.x + self.rows[3][1] * p.y + self.rows[3][2] * p.z + self.rows[3][3]

        if w != 1:
            x, y, z = x / w, y / w, z / w
        return Point3(x, y, z)
