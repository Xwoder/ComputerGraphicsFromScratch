from dataclasses import dataclass, field

from Rotation import Rotation
from Transform import Transform
from geometry.Vec3 import Vec3
from model.Model import Model


@dataclass
class Instance:
    """模型实例：把一个 Model 摆放（含位移）到世界空间。

    - model：被复用的网格（顶点 + 三角面，三角面自带 color）。多个 Instance
      可共享同一个 Model，仅以不同 transform 摆放，对应 Gabri Gambetta 的
      「物体复用 / 实例化（instancing）」思路。
    - transform：实例的局部变换（缩放 → 旋转 → 平移，默认单位变换）。实例在世界
      空间的整体位移也由 transform.translation 承担，因此无需单独的 position
      字段（否则永远只会是 Point3(0,0,0)，与 translation 重复）。

    渲染时，实例的实际顶点 = transform.apply(模型顶点)，再交给 Renderer 投影绘制。
    """

    model: Model
    transform: Transform = field(
        default_factory=lambda: Transform(1, Rotation(0, 0, 0), Vec3(0, 0, 0))
    )
