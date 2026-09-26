from Camera import Camera
from Canvas import Canvas
from Color import Color
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
        canvas = self._canvas
        scene = self._scene
        tracer = RayTracer(scene)
        viewport = self._viewport

        for y in range(canvas.height):
            for x in range(canvas.width):
                target: Point3 = Camera.canvasToViewport(
                    canvas,
                    viewport,
                    x,
                    y,
                )

                ray: Ray = Ray(
                    self._camera.origin,
                    target - self._camera.origin,
                )

                color: Color = tracer.traceRay(ray)
                canvas.putPixel(
                    x,
                    y,
                    color,
                )
