from dataclasses import dataclass, field
from typing import Optional

from model.Model import Model
from geometry.Point3 import Point3
from geometry.Vec3 import Vec3
from geometry.Matrix import Matrix
from Rotation import Rotation
from Transform import Transform


@dataclass
class Instance:
    """模型实例：把一个 Model 摆放到世界空间中由 position 指定的位置。

    - model：被复用的网格（顶点 + 三角面，三角面自带 color）。多个 Instance
      可共享同一个 Model，仅以不同 position 摆放，对应 Gabri Gambetta 的
      「物体复用 / 实例化（instancing）」思路。
    - position：实例在世界坐标系下的位置（相机在原点、看向 +z，故 z 需为正
      才能被正确透视投影）。它作为 transform 之后施加的整体平移。
    - transform：实例的局部变换（缩放 → 旋转 → 平移，默认单位变换），在叠加
      position 之前先作用于模型顶点，用于原地缩放 / 旋转模型。

    渲染时，实例的实际顶点 = transform.apply(模型顶点) + position，
    再交给 Rasterizer 投影绘制。
    """

    model: Model
    position: Point3
    transform: Transform = field(
        default_factory=lambda: Transform(1, Rotation(0, 0, 0), Vec3(0, 0, 0))
    )

    def applyTransform(self,
                       vertex: Point3,
                       transform: Optional[Transform] = None) -> Point3:
        """按「缩放 → 旋转 → 平移」把模型顶点变换到（局部）世界坐标。

        对应伪代码 ApplyTransform(vertex, transform)：
            scaled     = Scale(vertex, transform.scale)
            rotated    = Rotate(scaled, transform.rotation)
            translated = Translate(rotated, transform.translation)

        默认使用实例自身的 self.transform；也可显式传入其它 transform。
        注意：此处只施加局部变换，尚未叠加 instance.position 的整体世界平移
        （镜像 RenderInstance 中 transform 与 position 分开处理的设计）。
        """
        t: Transform = transform if transform is not None else self.transform

        # ❶ 均匀缩放（Point3 标量乘法）
        scaled: Point3 = vertex * t.scale

        # ❷ 欧拉角旋转（先 X，再 Y，最后 Z）；点 → 向量后做矩阵变换
        rotated: Vec3 = Matrix.rotation(
            (t.rotation.x, t.rotation.y, t.rotation.z)
        ).transform(scaled.to_vec3())

        # ❸ 局部平移（Vec3 + Vec3，再做位置点转换）
        shifted: Vec3 = rotated + t.translation
        return Point3(shifted.x, shifted.y, shifted.z)
