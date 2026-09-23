import math
from pathlib import Path

from Camera import Camera
from Canvas import Canvas
from Color import Color
from Interval import Interval
from Point3 import Point3
from Ray import Ray
from RayTracer import RayTracer
from Scene import Scene
from Sphere import Sphere
from Viewport import Viewport

CANVAS_WIDTH: int = 1600
CANVAS_HEIGHT: int = 1200
OUTPUT_PATH: Path = Path("output.ppm")


def createScene() -> Scene:
    """
    创建包含三个球体的场景：红、蓝、绿各一个。

    Returns:
        Scene: 由三个球体构成的场景
    """

    spheres: list[Sphere] = [
        Sphere(center=Point3(0, -1, 3), radius=1, color=Color(255, 0, 0)),
        Sphere(center=Point3(2, 0, 4), radius=1, color=Color(0, 0, 255)),
        Sphere(center=Point3(-2, 0, 4), radius=1, color=Color(0, 255, 0)),
    ]

    return Scene(spheres)


def render(scene: Scene,
           canvas: Canvas,
           camera: Camera,
           viewport: Viewport) -> None:
    """
    逐像素追踪光线并写入画布。

    对每个像素：画布坐标 -> 视口坐标 -> 由相机原点指向该点的射线 -> 求最近命中球。
    t 的有效区间取 [1, +inf)，即只接受位于视口前方（含视口平面之后）的交点。

    Args:
        scene (Scene): 待渲染场景。
        canvas (Canvas): 目标画布，渲染结果写入其中。
        camera (Camera): 相机，提供视线起点。
        viewport (Viewport): 视口，提供画布到世界的换算参数。
    """

    tracer: RayTracer = RayTracer(scene)
    interval: Interval = Interval(1, math.inf)

    for y in range(canvas.height):
        for x in range(canvas.width):
            target: Point3 = Camera.canvasToViewport(canvas, viewport, x, y)
            ray: Ray = Ray(camera.origin, target - camera.origin)

            canvas.putPixel(x, y, tracer.traceRay(ray, interval))


if __name__ == '__main__':
    canvas: Canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    # 视口宽高比与画布保持一致（800:600 = 4:3），避免图像被拉伸
    viewport: Viewport = Viewport(width=4, height=3, distance=1.0)
    camera: Camera = Camera()

    render(createScene(), canvas, camera, viewport)
    canvas.savePPM(OUTPUT_PATH)

    print(f"saved: {OUTPUT_PATH}")
