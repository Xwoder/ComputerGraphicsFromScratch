from dataclasses import dataclass

from Number import Number
from Rotation import Rotation
from geometry.Matrix import Matrix
from geometry.Point3 import Point3
from geometry.Vec3 import Vec3


@dataclass(frozen=True)
class Transform:
    """局部变换：以「缩放 → 旋转 → 平移」顺序作用于顶点。

    - scale：均匀缩放系数（标量，作用于三个轴）。
    - rotation：欧拉角（绕 X/Y/Z 轴的弧度），组合顺序与 Matrix.rotation 一致
      （先 X，再 Y，最后 Z）。
    - translation：局部平移偏移（在缩放/旋转之后施加）。

    单位变换为 Transform(1, Rotation(0,0,0), Vec3(0,0,0))，作用于任意点恒等不变。
    """

    scale: Number
    rotation: Rotation
    translation: Vec3

    def apply(self, vertex: Point3) -> Point3:
        """按「缩放 → 旋转 → 平移」把顶点变换到世界坐标点。

        对应伪代码 ApplyTransform(vertex, transform)：
            scaled     = Scale(vertex, scale)
            rotated    = Rotate(scaled, rotation)
            translated = Translate(rotated, translation)
        """
        # ❶ 均匀缩放（Point3 标量乘法）
        scaled: Point3 = vertex * self.scale

        # ❷ 欧拉角旋转（先 X，再 Y，最后 Z）；点 → 向量后做矩阵变换
        rotated: Vec3 = Matrix.rotation(
            (self.rotation.x, self.rotation.y, self.rotation.z)
        ).transform(scaled.to_vec3())

        # ❸ 局部平移（Vec3 + Vec3，再做位置点转换）
        shifted: Vec3 = rotated + self.translation
        return Point3(shifted.x, shifted.y, shifted.z)