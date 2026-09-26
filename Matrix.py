from __future__ import annotations

import math
from dataclasses import dataclass

from Number import Number
from Vec3 import Vec3


@dataclass(frozen=True)
class Matrix:
    """
    3×3 矩阵，目前只用于相机的朝向（旋转）。

    相机坐标系中，CanvasToViewport 算出的方向向量需要被这个矩阵变换到
    世界坐标系，才能使相机朝任意方向看。旋转矩阵是正交矩阵，保持向量
    长度与夹角不变，因此变换后的射线方向无需再次归一化。
    """

    rows: tuple[tuple[Number, ...], ...]

    def __post_init__(self):
        if not self.rows:
            raise ValueError("Matrix cannot be empty.")

        column_count = len(self.rows[0])

        if column_count == 0:
            raise ValueError("Matrix cannot have empty rows.")

        if any(len(row) != column_count for row in self.rows):
            raise ValueError("All rows must have the same length.")

        # 统一规整为不可变元组，匹配声明的 tuple[tuple[...]] 类型，
        # 同时让 frozen 实例真正不可变、可哈希。
        object.__setattr__(self, "rows", tuple(tuple(row) for row in self.rows))

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def column_count(self) -> int:
        return len(self.rows[0])

    def __getitem__(self, index: int) -> tuple[Number, ...]:
        return tuple(self.rows[index])

    @staticmethod
    def identity() -> Matrix:
        """单位矩阵：相机不旋转，看向 +z。"""
        return Matrix((
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
        ))

    @staticmethod
    def rotation_x(theta: Number) -> Matrix:
        c, s = math.cos(theta), math.sin(theta)
        return Matrix((
            (1, 0, 0),
            (0, c, -s),
            (0, s, c),
        ))

    @staticmethod
    def rotation_y(theta: Number) -> Matrix:
        c, s = math.cos(theta), math.sin(theta)
        return Matrix((
            (c, 0, s),
            (0, 1, 0),
            (-s, 0, c),
        ))

    @staticmethod
    def rotation_z(theta: Number) -> Matrix:
        c, s = math.cos(theta), math.sin(theta)
        return Matrix((
            (c, -s, 0),
            (s, c, 0),
            (0, 0, 1),
        ))

    @staticmethod
    def rotation(euler: tuple[Number, Number, Number]) -> Matrix:
        """
        由欧拉角（绕 X、Y、Z 轴的弧度）组合出旋转矩阵。
        组合顺序：先绕 X，再绕 Y，最后绕 Z（Rx · Ry · Rz）。
        """
        rx, ry, rz = euler
        return (
            Matrix.rotation_x(rx)
            .multiply(Matrix.rotation_y(ry))
            .multiply(Matrix.rotation_z(rz))
        )

    def __matmul__(self, other: Matrix) -> Matrix:
        """矩阵乘法运算符（A @ B），通用维度，要求 A 列数 == B 行数。"""
        if self.column_count != other.row_count:
            raise ValueError(
                "Matrix dimensions are incompatible for multiplication."
            )

        result = tuple(
            tuple(
                sum(
                    self[i][k] * other[k][j]
                    for k in range(self.column_count)
                )
                for j in range(other.column_count)
            )
            for i in range(self.row_count)
        )

        return type(self)(result)

    def multiply(self, other: Matrix) -> Matrix:
        """矩阵乘法（self · other），等价于 self @ other。"""
        return self @ other

    def transform(self, v: Vec3) -> Vec3:
        """
        把向量 v 当作列向量左乘本矩阵，返回变换后的向量
        （即 v 在世界坐标系下的表达）。
        """
        m = self.rows
        return Vec3(
            x=m[0][0] * v.x + m[0][1] * v.y + m[0][2] * v.z,
            y=m[1][0] * v.x + m[1][1] * v.y + m[1][2] * v.z,
            z=m[2][0] * v.x + m[2][1] * v.y + m[2][2] * v.z,
        )
