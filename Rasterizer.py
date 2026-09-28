from __future__ import annotations

from Camera import Camera
from Canvas import Canvas
from Canvas2D import Canvas2D
from Instance import Instance
from Viewport import Viewport
from color.Color import Color
from geometry.Point2 import Point2
from geometry.Point3 import Point3
from geometry.Triangle import Triangle
from geometry.Vec3 import Vec3


class Rasterizer:
    """栅格化渲染器：把「顶点 + 三角面」描述的 3D 网格投影到画布并绘制。

    对应 Gabriel Gambetta《Computer Graphics from Scratch》中把顶点透视投影
    （ProjectVertex）后用画线法绘制三角面的栅格化管线。与负责光线追踪的 Renderer
    解耦：这里不追踪射线，而是直接把网格投影成像素。

    流程（与 RenderObject/RenderTriangle 伪代码对齐）：
      - RenderObject：投影每个顶点 → 逐个三角面调用 RenderTriangle；
      - RenderTriangle：取该三角面三个投影后的画布坐标，连同面颜色交给
        DrawWireframeTriangle 画三条边（线框）；
      - 顶点投影由 Camera.projectVertex 完成（透视除 z + 视口→画布换算）。

    Attributes:
        _canvas / _camera / _viewport：渲染所需的画布与取景参数。
    """

    def __init__(self,
                 canvas: Canvas,
                 camera: Camera,
                 viewport: Viewport) -> None:
        """
        初始化栅格化渲染器，绑定渲染所需的画布与取景参数。

        Args:
            canvas (Canvas): 目标画布，渲染结果写入其中。
            camera (Camera): 相机，提供视线起点（用于背面剔除判断朝向）。
            viewport (Viewport): 视口，提供投影所需的世界尺寸与距离。
        """

        self._canvas = canvas
        self._camera = camera
        self._viewport = viewport

    def renderObject(
            self,
            vertices: list[Point3],
            triangles: list[Triangle],
            *,
            backFaceCulling: bool = False,
    ) -> None:
        """投影顶点并逐个三角面绘制，渲染一个 3D 网格物体。

        流程与 RenderObject(vertices, triangles) 伪代码对齐：
          ❶ 把每个顶点透视投影到画布像素坐标（ProjectVertex）；
          ❷ 逐个三角面调用 renderTriangle 绘制（可开启背面剔除）。

        Args:
            vertices: 相机空间下的顶点列表（Point3 位置点）。
            triangles: 三角面列表，每个元素为 Triangle（含 v 下标与 color）。
            backFaceCulling: 是否开启背面剔除（默认关闭）。线框模式通常显示全部棱边；
                开启后只绘制朝向相机的三角面（对凸网格更清晰）。
        """

        # ❶ 把每个顶点透视投影到画布像素坐标（ProjectVertex）
        projected: list[Point2] = [
            Camera.projectVertex(self._canvas, self._viewport, v)
            for v in vertices
        ]

        # ❷ 逐个三角面绘制（RenderTriangle）
        for triangle in triangles:
            # 背面剔除：跳过背对相机的三角面
            if backFaceCulling and self._isBackFacing(triangle, vertices):
                continue
            self.renderTriangle(triangle, projected)

    def renderInstances(self, instances: list[Instance]) -> None:
        """渲染一组模型实例（instancing）。

        每个 Instance 由 (model, position, transform) 组成：先把模型顶点按局部
        transform（缩放 → 旋转 → 平移）变换，再整体平移到实例所在的世界位置
        position（顶点 = transform.apply(模型顶点) + position），最后交给
        renderObject 投影绘制。多个 Instance 可共享同一个 Model，仅以不同
        transform / position 摆放，实现物体复用。

        Args:
            instances: 实例列表，每个元素为 Instance（含 model、position、transform）。
        """
        for inst in instances:
            offset: Vec3 = inst.position.to_vec3()
            # 先对模型顶点施加局部变换（缩放/旋转/平移），
            # 再整体平移到实例的世界位置（position 即世界坐标，相机在原点看向 +z）
            world_vertices: list[Point3] = [
                inst.transform.apply(v) + offset for v in inst.model.vertices
            ]
            self.renderObject(world_vertices, inst.model.triangles)

    def renderTriangle(self,
                       triangle: Triangle,
                       projected: list[Point2]) -> None:
        """绘制单个三角面：取三个投影顶点连同面颜色，交给 DrawWireframeTriangle。

        对应 RenderTriangle(triangle, projected)：
            DrawWireframeTriangle(projected[triangle.vertex_indices[0]],
                                  projected[triangle.vertex_indices[1]],
                                  projected[triangle.vertex_indices[2]],
                                  triangle.color)
        """
        DrawWireframeTriangle(projected[triangle.vertex_indices[0]],
                              projected[triangle.vertex_indices[1]],
                              projected[triangle.vertex_indices[2]],
                              triangle.color,
                              self)

    def _isBackFacing(self,
                      triangle: Triangle,
                      vertices: list[Point3]) -> bool:
        """判断三角面是否背对相机（需剔除）。

        用相机空间下的三个顶点算几何法向 N = (B-A) × (C-A)，相机位于原点，
        三角面朝向相机当且仅当 N·(origin - A) > 0（即 N·A < 0）。返回 True 表示
        背对（应被剔除）。该法向测试与投影后的屏幕朝向无关，对凸网格稳定可靠。
        """
        a, b, c = (vertices[i] for i in triangle.vertex_indices)
        ab = b - a  # Point3 - Point3 -> Vec3
        ac = c - a

        # 叉积 (B-A) × (C-A)
        nx = ab.y * ac.z - ab.z * ac.y
        ny = ab.z * ac.x - ab.x * ac.z
        nz = ab.x * ac.y - ab.y * ac.x

        # N·A >= 0 视为背对相机
        return (nx * a.x + ny * a.y + nz * a.z) >= 0

    def _putPixelSafe(self,
                      x: float,
                      y: float,
                      color: Color) -> None:
        """带边界检查的写像素：越界（投影到画布外）的栅格单元直接忽略。"""
        xi = round(x)
        yi = round(y)
        if 0 <= xi < self._canvas.width and 0 <= yi < self._canvas.height:
            self._canvas.putPixel(xi, yi, color)


def DrawWireframeTriangle(p0: Point2,
                          p1: Point2,
                          p2: Point2,
                          color: Color,
                          rasterizer: Rasterizer) -> None:
    """线框三角形：用 color 画出三角形的三条边（p0→p1→p2→p0）。

    每条边复用 Canvas2D.draw_line（对称直线栅格化）得到被点亮的栅格单元，
    再逐格安全写入 3D Canvas 像素缓冲。
    """
    for a, b in ((p0, p1), (p1, p2), (p2, p0)):
        for cell in Canvas2D.draw_line(a, b):
            rasterizer._putPixelSafe(cell.x, cell.y, color)
