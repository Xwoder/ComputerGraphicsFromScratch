from dataclasses import dataclass, field

from Number import Number
from Canvas import Canvas
from geometry.Matrix import Matrix
from geometry.Point2 import Point2
from geometry.Point3 import Point3
from geometry.Vec3 import Vec3
from Viewport import Viewport


@dataclass
class Camera:
    """
    相机：提供视线起点（origin）与朝向（rotation）。

    - origin：相机在世界坐标系中的位置。
    - rotation：3×3 旋转矩阵（Matrix），把视口局部方向变换到世界方向。
      默认单位矩阵，即相机不旋转、看向 +z（与旧版行为一致）。
    """

    origin: Point3 = Point3(0, 0, 0)
    rotation: Matrix = field(default_factory=Matrix.identity)

    @staticmethod
    def canvasToViewport(
            canvas: Canvas,
            viewport: Viewport,
            canvasX: int,
            canvasY: int,
    ) -> Point3:
        """
        把画布像素坐标换算到视口（相机局部）坐标。

        - 画布原点在左上角、y 轴向下；视口原点在中心、y 轴向上，
          故 x 需要减去半个画布宽、y 需要取 (半高 - canvasY) 再缩放。
        - 缩放因子为视口世界尺寸 / 画布像素尺寸（viewport.width/canvas.width、
          viewport.height/canvas.height），在内部直接计算，调用方无需关心。
        - z 恒为视口到相机的距离。

        Args:
            canvas (Canvas): 当前画布，提供像素尺寸。
            viewport (Viewport): 视口，提供世界尺寸与距离。
            canvasX (int): 像素列号，取值 [0, canvas.width)。
            canvasY (int): 像素行号，取值 [0, canvas.height)。

        Returns:
            Point3: 该像素中心在视口平面上的坐标（相机局部坐标系）。
        """

        scaleX = viewport.width / canvas.width
        scaleY = viewport.height / canvas.height

        viewportX = (canvasX - canvas.width / 2) * scaleX
        viewportY = (canvas.height / 2 - canvasY) * scaleY
        viewportZ = viewport.distance

        return Point3(x=viewportX, y=viewportY, z=viewportZ)

    @staticmethod
    def viewportToCanvas(
            canvas: Canvas,
            viewport: Viewport,
            viewportX: Number,
            viewportY: Number,
    ) -> Point2:
        """
        Camera.canvasToViewport 的逆运算：把视口（相机局部）坐标换算回画布像素坐标。

        - 复用与 canvasToViewport 完全一致的缩放因子（viewport.width/canvas.width、
          viewport.height/canvas.height），把视口平面上的 (viewportX, viewportY)
          映射回画布原点在左上角、y 轴向下的像素坐标。
        - 这是把“投影后的视口坐标”落回屏幕像素的关键一步，供 ProjectVertex 调用。

        Args:
            canvas (Canvas): 当前画布，提供像素尺寸。
            viewport (Viewport): 视口，提供世界尺寸。
            viewportX (Number): 视口平面上的 x 坐标（相机局部坐标系）。
            viewportY (Number): 视口平面上的 y 坐标（相机局部坐标系）。

        Returns:
            Point2: 对应的画布像素坐标（可能为小数，交给 putPixel 前按需 round）。
        """

        scaleX = viewport.width / canvas.width
        scaleY = viewport.height / canvas.height

        canvasX = viewportX / scaleX + canvas.width / 2
        canvasY = canvas.height / 2 - viewportY / scaleY

        return Point2(x=canvasX, y=canvasY)

    @staticmethod
    def projectVertex(
            canvas: Canvas,
            viewport: Viewport,
            vertex: Vec3,
    ) -> Point2:
        """
        透视投影：把相机空间下的 3D 顶点投影到画布像素坐标。

        先将相机空间顶点 v 透视除 z，投到距离相机 d（viewport.distance）的视口平面，
        得到视口坐标 (v.x * d / v.z, v.y * d / v.z)，再由 ViewportToCanvas 换算成
        画布像素坐标。对应 Gabriel Gambetta《Computer Graphics from Scratch》的
        ProjectVertex；此处 d 取 viewport.distance，并以静态方法显式传入 canvas/viewport。

        Args:
            canvas (Canvas): 当前画布，提供像素尺寸。
            viewport (Viewport): 视口，提供世界尺寸与到相机的距离 d。
            vertex (Vec3): 相机空间下的 3D 顶点。

        Returns:
            Point2: 投影后的画布像素坐标（可能为小数，交给 putPixel 前按需 round）。
        """

        d = viewport.distance
        return Camera.viewportToCanvas(
            canvas, viewport, vertex.x * d / vertex.z, vertex.y * d / vertex.z)
