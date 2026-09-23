from Canvas import Canvas
from Point3 import Point3
from Vec3 import Vec3
from Viewport import Viewport


class Camera:
    _origin: Point3 = Point3(0, 0, 0)
    _direction: Vec3 = Vec3(0, 0, 1)

    @property
    def origin(self) -> Point3:
        """
        相机位置（即所有视线的起点，只读属性）。

        Returns:
            Point3: 相机所在的三维点
        """
        return self._origin

    def __repr__(self) -> str:
        """
        返回相机的官方字符串表示，形如 Camera(center=..., direction=...)。
        供 repr()、交互式解释器及调试使用。

        Returns:
            str: 包含相机位置与朝向的字符串表示
        """
        return (f"Camera("
                f"center={self._origin!r}, "
                f"direction={self._direction!r})")

    @staticmethod
    def canvasToViewport(
            canvas: Canvas,
            viewport: Viewport,
            canvasX: int,
            canvasY: int
    ) -> Point3:

        viewportX = canvasX * viewport.width / canvas.width
        viewportY = canvasY * viewport.height / canvas.height
        viewportZ = viewport.distance

        return Point3(x=viewportX, y=viewportY, z=viewportZ)
