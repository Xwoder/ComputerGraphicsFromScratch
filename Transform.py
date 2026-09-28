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

    def apply(self, point: Point3) -> Point3:
        """把 point 按「缩放 → 旋转 → 平移」变换到新的世界坐标点。"""
        # ❶ 均匀缩放
        scaled: Vec3 = Vec3(point.x * self.scale,
                            point.y * self.scale,
                            point.z * self.scale)

        # ❷ 欧拉角旋转（Rx · Ry · Rz）
        rotated: Vec3 = Matrix.rotation(
            (self.rotation.x, self.rotation.y, self.rotation.z)
        ).transform(scaled)

        # ❸ 平移
        return Point3(rotated.x + self.translation.x,
                      rotated.y + self.translation.y,
                      rotated.z + self.translation.z)