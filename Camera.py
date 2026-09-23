from dataclasses import dataclass

from Canvas import Canvas
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
            canvasY: int
    ) -> Point3:
        """
        把画布像素坐标换算到视口（相机局部）坐标。

        - 画布原点在左上角、y 轴向下；视口原点在中心、y 轴向上，
          故 x 需要减去半个画布宽、y 需要取 (半高 - canvasY) 再缩放。
        - z 恒为视口到相机的距离。

        Args:
            canvas (Canvas): 当前画布，提供像素尺寸。
            viewport (Viewport): 视口，提供世界尺寸与距离。
            canvasX (int): 像素列号，取值 [0, canvas.width)。
            canvasY (int): 像素行号，取值 [0, canvas.height)。

        Returns:
            Point3: 该像素中心在视口平面上的坐标（相机局部坐标系）。
        """

        viewportX = (canvasX - canvas.width / 2) * viewport.width / canvas.width
        viewportY = (canvas.height / 2 - canvasY) * viewport.height / canvas.height
        viewportZ = viewport.distance

        return Point3(x=viewportX, y=viewportY, z=viewportZ)
