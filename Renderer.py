from Camera import Camera
from Canvas import Canvas
from Instance import Instance
from Rasterizer import DrawWireframeTriangle
from Ray import Ray
from RayTracer import RayTracer
from Scene import Scene
from color.Color import Color
from geometry.Matrix4 import Matrix4
from geometry.Point2 import Point2
from geometry.Point3 import Point3
from geometry.Triangle import Triangle
from geometry.Vec3 import Vec3
from model.Model import Model
from Viewport import Viewport


class Renderer:
    """统一渲染器：同时支持光线追踪（render）与栅格化实例渲染（render_scene / render_model）。"""

    _scene: Scene | None
    _canvas: Canvas
    _camera: Camera
    _viewport: Viewport

    def __init__(self,
                 scene: Scene | None,
                 canvas: Canvas,
                 camera: Camera,
                 viewport: Viewport):
        """
        初始化渲染器，绑定渲染所需的场景与取景参数。

        Args:
            scene (Scene | None): 待渲染场景（光追用）；栅格化实例渲染可传 None。
            canvas (Canvas): 目标画布，渲染结果写入其中。
            camera (Camera): 相机，提供视线起点与朝向。
            viewport (Viewport): 视口，提供画布到世界的换算参数。
        """

        self._scene = scene
        self._canvas = canvas
        self._camera = camera
        self._viewport = viewport

    def render(self) -> None:
        assert self._scene is not None, "光线追踪需要先提供 scene"
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

                # CanvasToViewport 给的是相机局部坐标系下的方向（z = 视口距离），
                # 用相机朝向矩阵旋转到世界坐标系，再从相机位置发出射线。
                direction: Vec3 = self._camera.rotation.transform(
                    Vec3(target.x, target.y, target.z),
                )
                ray: Ray = Ray(self._camera.origin, direction)

                color: Color = tracer.traceRay(ray)
                canvas.putPixel(
                    x,
                    y,
                    color,
                )

    # ───────────────────────── 栅格化实例渲染 ─────────────────────────

    def project_vertex(self, world_vertex: Point3) -> Point2:
        """把世界坐标点透视投影到画布像素坐标（委托 Camera.projectVertex）。"""
        return Camera.projectVertex(self._canvas, self._viewport, world_vertex)

    def _putPixelSafe(self, x: float, y: float, color: Color) -> None:
        """带边界检查的写像素：越界（投影到画布外）的栅格单元直接忽略。"""
        xi = round(x)
        yi = round(y)
        if 0 <= xi < self._canvas.width and 0 <= yi < self._canvas.height:
            self._canvas.putPixel(xi, yi, color)

    def render_triangle(self, triangle: Triangle, projected: list[Point2]) -> None:
        """绘制单个三角面：取三个投影顶点连同面颜色，交给 DrawWireframeTriangle。"""
        DrawWireframeTriangle(projected[triangle.vertex_indices[0]],
                              projected[triangle.vertex_indices[1]],
                              projected[triangle.vertex_indices[2]],
                              triangle.color,
                              self)

    def render_model(self, model: Model, transform: Matrix4) -> None:
        """渲染单个模型（对齐 RenderModel(model, transform) 伪代码）。

        用单个合成矩阵 transform 把每个顶点一次性变换到相机空间
        （transform * V），再透视投影，最后逐三角面绘制。
        """
        projected: list[Point2] = [
            self.project_vertex(transform.transform_point(vertex))
            for vertex in model.vertices
        ]

        for triangle in model.triangles:
            self.render_triangle(triangle, projected)

    def render_scene(self, instances: list[Instance]) -> None:
        """渲染一组实例（对齐 RenderScene() 伪代码）。

        构建世界→相机矩阵 M_camera，对每个实例合成 M = M_camera · I.transform，
        再交给 render_model 绘制。本项目的 Scene 以 spheres 存放光追物体，instances
        由调用方持有，故此处显式接收 instances 列表（对应伪代码里的 scene.instances）。
        """
        m_camera = self._camera.make_camera_matrix()
        for inst in instances:
            m = m_camera @ inst.transform.to_matrix4()
            self.render_model(inst.model, m)
