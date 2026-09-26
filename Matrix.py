import math
from dataclasses import dataclass

from Number import Number
from Vec3 import Vec3


@dataclass
class Matrix:
    """
    3×3 矩阵，目前只用于相机的朝向（旋转）。

    相机坐标系中，CanvasToViewport 算出的方向向量需要被这个矩阵变换到
    世界坐标系，才能使相机朝任意方向看。旋转矩阵是正交矩阵，保持向量
    长度与夹角不变，因此变换后的射线方向无需再次归一化。
    """

    m: list[list[Number]]

    @staticmethod
    def identity() -> "Matrix":
        """单位矩阵：相机不旋转，看向 +z。"""
        return Matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ])

    @staticmethod
    def rotation_x(theta: Number) -> "Matrix":
        c, s = math.cos(theta), math.sin(theta)
        return Matrix([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c],
        ])

    @staticmethod
    def rotation_y(theta: Number) -> "Matrix":
        c, s = math.cos(theta), math.sin(theta)
        return Matrix([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c],
        ])

    @staticmethod
    def rotation_z(theta: Number) -> "Matrix":
        c, s = math.cos(theta), math.sin(theta)
        return Matrix([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1],
        ])

    @staticmethod
    def rotation(euler: tuple[Number, Number, Number]) -> "Matrix":
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

    def multiply(self, other: "Matrix") -> "Matrix":
        """矩阵乘法（self · other）。"""
        a, b = self.m, other.m
        return Matrix([[
            a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j]
            for j in range(3)
        ] for i in range(3)])

    def transform(self, v: Vec3) -> Vec3:
        """
        把向量 v 当作列向量左乘本矩阵，返回变换后的向量
        （即 v 在世界坐标系下的表达）。
        """
        m = self.m
        return Vec3(
            x=m[0][0] * v.x + m[0][1] * v.y + m[0][2] * v.z,
            y=m[1][0] * v.x + m[1][1] * v.y + m[1][2] * v.z,
            z=m[2][0] * v.x + m[2][1] * v.y + m[2][2] * v.z,
        )
