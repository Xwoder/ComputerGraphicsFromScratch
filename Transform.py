from dataclasses import dataclass

from Number import Number
from Rotation import Rotation
from geometry.Matrix4 import Matrix4
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

    def apply(self, point: Point3) -> Point3:
        """按「缩放 → 旋转 → 平移」把顶点变换到世界坐标点。

        对应伪代码 ApplyTransform(vertex, transform)：
            scaled     = Scale(vertex, scale)
            rotated    = Rotate(scaled, rotation)
            translated = Translate(rotated, translation)
        """
        scaled = point * self.scale
        rotated = self.rotation.apply(scaled)
        return rotated + self.translation

    def to_matrix4(self) -> Matrix4:
        """把分解式变换（缩放 → 旋转 → 平移）合成为单个 4×4 齐次矩阵。

        等价于 apply：M = T(translation) · R(rotation) · S(scale)，
        于是 M · v == apply(v)。供 RenderScene 与相机矩阵合成使用。
        """
        return (
            Matrix4.translation(self.translation.x, self.translation.y, self.translation.z)
            @ Matrix4.rotation((self.rotation.x, self.rotation.y, self.rotation.z))
            @ Matrix4.scaling(self.scale)
        )