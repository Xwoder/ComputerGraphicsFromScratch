from dataclasses import dataclass

from Point3 import Point3


@dataclass(frozen=True)
class Camera:
    center: Point3 = Point3(0, 0, 0)

    def __repr__(self) -> str:
        return f"Camera(center={self.center!r})"
