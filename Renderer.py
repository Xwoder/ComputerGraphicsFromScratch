from Camera import Camera
from Canvas import Canvas
from Instance import Instance
from Rasterizer import PixelWriter
from Ray import Ray
from RayTracer import RayTracer
from RayTracingScene import RayTracingScene
from RasterizationScene import RasterizationScene
from color.Color import Color
from geometry.Point2 import Point2
from geometry.Point3 import Point3
from geometry.Triangle import Triangle
from geometry.Vec3 import Vec3
from Viewport import Viewport


class Renderer(PixelWriter):
    """统一渲染器：同时支持光线追踪（render）与栅格化实例渲染（render_scene / render_instance）。

    camera / viewport 由 Renderer 持有并供两条管线共用（光追用它发射射线，
    栅格化用它构造 M_camera 与透视投影），因此不塞进某个 Scene 子类。
    """

    _scene: RayTracingScene | RasterizationScene
    _canvas: Canvas
    _camera: Camera
    _viewport: Viewport

    def __init__(self,
                 scene: RayTracingScene | RasterizationScene,
                 canvas: Canvas,
                 camera: Camera,
                 viewport: Viewport):
        """
        初始化渲染器，绑定渲染所需的场景与取景参数。

        Args:
            scene: 待渲染场景。光线追踪传 RayTracingScene（含 spheres）；
                栅格化实例渲染传 RasterizationScene（含 instances）。
            canvas (Canvas): 目标画布，渲染结果写入其中。
            camera (Camera): 相机，提供视线起点与朝向（两条管线共用）。
            viewport (Viewport): 视口，提供画布到世界的换算参数（两条管线共用）。
        """

        self._scene = scene
        self._canvas = canvas
        self._camera = camera
        self._viewport = viewport

    def render(self) -> None:
        assert isinstance(self._scene, RayTracingScene), "光线追踪需要先提供 RayTracingScene"
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

    def render_triangle(self, triangle: Triangle, projected: list[Point2]) -> None:
        """绘制单个三角面：取三个投影顶点连同面颜色，交给 draw_wireframe_triangle。"""
        self.draw_wireframe_triangle(projected[triangle.vertex_indices[0]],
                                     projected[triangle.vertex_indices[1]],
                                     projected[triangle.vertex_indices[2]],
                                     triangle.color)

    def render_instance(self, instance: Instance) -> None:
        """渲染单个模型实例（对齐 RenderInstance(instance) 伪代码）。

            projected = []
            for V in instance.model.vertices:
                V' = ApplyTransform(V, instance.transform)   # instance.transform.apply(V)
                projected.append(ProjectVertex(V'))          # self.project_vertex
            for T in instance.model.triangles:
                RenderTriangle(T, projected)                 # self.render_triangle

        每个顶点先经 transform（缩放→旋转→平移）变换到世界坐标，再透视投影，
        最后逐三角面用线框绘制。
        """
        model = instance.model

        # 投影每个变换后的顶点（ApplyTransform + ProjectVertex）
        projected: list[Point2] = []
        for vertex in model.vertices:
            world_vertex: Point3 = instance.transform.apply(vertex)
            projected.append(self.project_vertex(world_vertex))

        # 逐个三角面绘制（RenderTriangle）
        for triangle in model.triangles:
            self.render_triangle(triangle, projected)

    def render_scene(self) -> None:
        """渲染场景中的全部实例（对齐 RenderScene() 伪代码）。

            RenderScene() {
                for I in scene.instances {
                    RenderInstance(I);
                }
            }

        遍历 scene.instances，对每个实例调用 render_instance 绘制。
        """
        assert isinstance(self._scene, RasterizationScene), \
            "栅格化实例渲染需要先提供带 instances 的 RasterizationScene"
        for inst in self._scene.instances:
            self.render_instance(inst)
