from dataclasses import dataclass, field

from color.Color import Color
from Instance import Instance


@dataclass
class RasterizationScene:
    """栅格化场景：实例（模型实例化）与未命中时的背景色。

    对应书里画线框立方体章节的 scene——核心是 instances，由 Renderer.render_scene
    遍历绘制（对齐 RenderScene() { for I in scene.instances { RenderInstance(I); } }）。
    它不认识光追的 spheres；线框渲染不做光照，故无 lights 字段。
    """

    instances: list[Instance] = field(default_factory=list)

    BACKGROUND_COLOR: Color = Color.BLACK
