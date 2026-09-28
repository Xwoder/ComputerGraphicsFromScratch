from dataclasses import dataclass, field

from Rotation import Rotation
from Transform import Transform
from geometry.Point3 import Point3
from geometry.Vec3 import Vec3
from model.Model import Model


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
    再交给 Renderer 投影绘制。
    """

    model: Model
    position: Point3
    transform: Transform = field(
        default_factory=lambda: Transform(1, Rotation(0, 0, 0), Vec3(0, 0, 0))
    )
