from dataclasses import dataclass

from Canvas import Canvas
from Number import Number
from Point3 import Point3
from Viewport import Viewport


@dataclass
class Camera:
    """
    相机：提供视线起点（origin）。
    """

    origin: Point3 = Point3(0, 0, 0)

    @staticmethod
    def canvasToViewport(
            canvas: Canvas,
            viewport: Viewport,
            canvasX: int,
            canvasY: int,
            scaleX: Number | None = None,
            scaleY: Number | None = None,
    ) -> Point3:
        """
        把画布像素坐标换算到视口（相机局部）坐标。

        - 画布原点在左上角、y 轴向下；视口原点在中心、y 轴向上，
          故 x 需要减去半个画布宽、y 需要取 (半高 - canvasY) 再缩放。
        - z 恒为视口到相机的距离。
        - scaleX/scaleY 为可选的预计算缩放因子（viewport.width/canvas.width、
          viewport.height/canvas.height）。由 Renderer 在整图渲染前算好并传入，
          避免每个像素重复做浮点除法；不传时回退为实时计算，便于独立调用与测试。

        Args:
            canvas (Canvas): 当前画布，提供像素尺寸。
            viewport (Viewport): 视口，提供世界尺寸与距离。
            canvasX (int): 像素列号，取值 [0, canvas.width)。
            canvasY (int): 像素行号，取值 [0, canvas.height)。
            scaleX (Number | None): 预计算的 X 缩放因子；为 None 时按 viewport/canvas 实时计算。
            scaleY (Number | None): 预计算的 Y 缩放因子；为 None 时按 viewport/canvas 实时计算。

        Returns:
            Point3: 该像素中心在视口平面上的坐标（相机局部坐标系）。
        """

        if scaleX is None:
            scaleX = viewport.width / canvas.width
        if scaleY is None:
            scaleY = viewport.height / canvas.height

        viewportX = (canvasX - canvas.width / 2) * scaleX
        viewportY = (canvas.height / 2 - canvasY) * scaleY
        viewportZ = viewport.distance

        return Point3(x=viewportX, y=viewportY, z=viewportZ)
