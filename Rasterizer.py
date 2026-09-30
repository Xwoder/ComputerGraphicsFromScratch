from __future__ import annotations

from Camera import Camera
from Canvas import Canvas
from Canvas2D import Canvas2D
from Viewport import Viewport
from color.Color import Color
from geometry.Matrix4 import Matrix4
from geometry.Point2 import Point2
from geometry.Point3 import Point3
from geometry.Triangle import Triangle


class PixelWriter:
    """线框三角面绘制所需的像素写入基类，Rasterizer 与 Renderer 均继承。

    提供统一的带边界检查写像素（_putPixelSafe）与线框三角形绘制
    （draw_wireframe_triangle，对应原模块级函数 DrawWireframeTriangle）。
    子类只需在 __init__ 中设置 self._canvas。
    """

    _canvas: Canvas

    def _putPixelSafe(self, x: float, y: float, color: Color) -> None:
        """带边界检查的写像素：越界（投影到画布外）的栅格单元直接忽略。"""
        xi = round(x)
        yi = round(y)
        if 0 <= xi < self._canvas.width and 0 <= yi < self._canvas.height:
            self._canvas.putPixel(xi, yi, color)

    def draw_wireframe_triangle(self,
                                p0: Point2,
                                p1: Point2,
                                p2: Point2,
                                color: Color) -> None:
        """线框三角形：用 color 画出三角形的三条边（p0→p1→p2→p0）。

        每条边复用 Canvas2D.draw_line（对称直线栅格化）得到被点亮的栅格单元，
        再逐格安全写入 3D Canvas 像素缓冲。
        """
        for a, b in ((p0, p1), (p1, p2), (p2, p0)):
            for cell in Canvas2D.draw_line(a, b):
                self._putPixelSafe(cell.x, cell.y, color)


class Rasterizer(PixelWriter):
    """栅格化渲染器：把「顶点 + 三角面」描述的 3D 网格投影到画布并绘制。

    对应 Gabriel Gambetta《Computer Graphics from Scratch》中把顶点透视投影
    （ProjectVertex）后用画线法绘制三角面的栅格化管线。与负责光线追踪的 Renderer
    解耦：这里不追踪射线，而是直接把网格投影成像素。

    流程（与 RenderObject/RenderTriangle 伪代码对齐）：
      - RenderObject：投影每个顶点 → 逐个三角面调用 RenderTriangle；
      - RenderTriangle：取该三角面三个投影后的画布坐标，连同面颜色交给
        draw_wireframe_triangle 画三条边（线框）；
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
            transform: Matrix4 = Matrix4.identity(),
    ) -> None:
        """投影顶点并逐个三角面绘制，渲染一个 3D 网格物体。

        流程与 RenderObject(vertices, triangles) 伪代码对齐，并补齐第10章
        Listing 10-5 的相机矩阵合成（此前只把顶点当相机空间直接投影，导致
        相机移动/旋转后结果错误，与 Renderer 修复前同一问题）：

          ❶ 合成世界→相机矩阵 M = M_camera · transform，把每个顶点（世界/模型
             空间）变换到相机空间，再透视投影到画布像素坐标（ProjectVertex）；
          ❷ 逐个三角面调用 renderTriangle 绘制。

        Args:
            vertices: 物体的顶点（世界坐标系，或模型坐标系配合 transform）。
            triangles: 三角面列表（自带顶点索引与颜色）。
            transform: 顶点从模型/世界空间到「相机空间前」的附加变换矩阵，
                默认单位矩阵。若传入实例变换矩阵 I.transform，则等价于
                M = M_camera · I.transform，与 Renderer 渲染实例的语义一致。
        """

        # ❶ 合成世界→相机矩阵，变换顶点后再投影
        camera_matrix: Matrix4 = self._camera.make_camera_matrix()
        M: Matrix4 = camera_matrix @ transform

        projected: list[Point2] = [
            Camera.projectVertex(self._canvas, self._viewport, M.transform_point(vex))
            for vex in vertices
        ]

        # ❷ 逐个三角面绘制（RenderTriangle）
        for triangle in triangles:
            self.renderTriangle(triangle, projected)

    def renderTriangle(self,
                       triangle: Triangle,
                       projected: list[Point2]) -> None:
        """绘制单个三角面：取三个投影顶点连同面颜色，交给 draw_wireframe_triangle。

        对应 RenderTriangle(triangle, projected)：
            draw_wireframe_triangle(projected[triangle.vertex_indices[0]],
                                    projected[triangle.vertex_indices[1]],
                                    projected[triangle.vertex_indices[2]],
                                    triangle.color)
        """
        self.draw_wireframe_triangle(projected[triangle.vertex_indices[0]],
                                     projected[triangle.vertex_indices[1]],
                                     projected[triangle.vertex_indices[2]],
                                     triangle.color)
