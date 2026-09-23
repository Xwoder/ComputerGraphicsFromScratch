import math

from Camera import Camera
from Canvas import Canvas
from Interval import Interval
from Point3 import Point3
from Ray import Ray
from RayTracer import RayTracer
from Scene import Scene
from Viewport import Viewport


class Renderer:
    _scene: Scene
    _canvas: Canvas
    _camera: Camera
    _viewport: Viewport

    def __init__(self,
                 scene: Scene,
                 canvas: Canvas,
                 camera: Camera,
                 viewport: Viewport):
        """
        初始化渲染器，绑定渲染所需的场景与取景参数。

        Args:
            scene (Scene): 待渲染场景。
            canvas (Canvas): 目标画布，渲染结果写入其中。
            camera (Camera): 相机，提供视线起点。
            viewport (Viewport): 视口，提供画布到世界的换算参数。
        """

        self._scene = scene
        self._canvas = canvas
        self._camera = camera
        self._viewport = viewport

    def render(self) -> None:
        """
        逐像素追踪光线并写入画布。

        对每个像素：画布坐标 -> 视口坐标 -> 由相机原点指向该点的射线 -> 求最近命中球。
        t 的有效区间取 [1, +inf)，即只接受位于视口前方（含视口平面之后）的交点。
        """

        tracer: RayTracer = RayTracer(self._scene)
        interval: Interval = Interval(1, math.inf)

        canvas: Canvas = self._canvas

        for col in range(canvas.height):
            for row in range(canvas.width):
                target: Point3 = Camera.canvasToViewport(
                    canvas,
                    self._viewport,
                    row,
                    col,
                )
                ray: Ray = Ray(self._camera.origin, target - self._camera.origin)

                canvas.putPixel(row, col, tracer.traceRay(ray, interval))
