from Point3 import Point3
from Vec3 import Vec3


class Camera:
    _center: Point3 = Point3(0, 0, 0)
    _direction: Vec3 = Vec3(0, 0, -1)

    def __repr__(self) -> str:
        """
        返回相机的官方字符串表示，形如 Camera(center=..., direction=...)。
        供 repr()、交互式解释器及调试使用。

        Returns:
            str: 包含相机位置与朝向的字符串表示
        """
        return (f"Camera("
                f"center={self._center!r}, "
                f"direction={self._direction!r})")
