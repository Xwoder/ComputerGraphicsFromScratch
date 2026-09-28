from dataclasses import dataclass

from model.Model import Model
from geometry.Point3 import Point3


@dataclass
class Instance:
    """模型实例：把一个 Model 摆放到世界空间中由 position 指定的位置。

    - model：被复用的网格（顶点 + 三角面，三角面自带 color）。多个 Instance
      可共享同一个 Model，仅以不同 position 摆放，对应 Gabri Gambetta 的
      「物体复用 / 实例化（instancing）」思路。
    - position：实例在世界坐标系下的位置（相机在原点、看向 +z，故 z 需为正
      才能被正确透视投影）。

    渲染时，实例的实际顶点 = 模型顶点 + position，再交给 Rasterizer 投影绘制。
    """

    model: Model
    position: Point3
