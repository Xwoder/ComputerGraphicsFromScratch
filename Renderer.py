from Camera import Camera
from Canvas import Canvas
from Instance import Instance
from Rasterizer import PixelWriter
from Ray import Ray
from RayTracer import RayTracer
from RayTracingScene import RayTracingScene
from RasterizationScene import RasterizationScene
from color.Color import Color
from geometry.Matrix4 import Matrix4
from geometry.Point2 import Point2
from geometry.Point3 import Point3
from geometry.Triangle import Triangle
from geometry.Vec3 import Vec3
from model.Model import Model
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

    def render_model(self, model: Model, transform: Matrix4) -> None:
        """用变换矩阵把模型顶点变换到相机空间并逐面绘制（对齐 Listing 10-5 的 RenderModel）。

            for V in model.vertices:
                projected.append(ProjectVertex(transform * V))
            for T in model.triangles:
                RenderTriangle(T, projected)

        transform 为世界→相机空间的合成矩阵 M（= M_camera * I.transform）。
        顶点经 M 变换到相机空间后再透视投影，最后逐三角面用线框绘制。
        """
        # 投影每个顶点（M * V 变换到相机空间，再 ProjectVertex）
        projected: list[Point2] = [
            self.project_vertex(transform.transform_point(vertex))
            for vertex in model.vertices
        ]

        # 逐个三角面绘制（RenderTriangle）
        for triangle in model.triangles:
            self.render_triangle(triangle, projected)

    def render_instance(self, instance: Instance) -> None:
        """渲染单个模型实例（对齐 RenderInstance / Listing 10-5 的矩阵合成版）。

            RenderScene() {
                M_camera = MakeCameraMatrix(camera)
                for I in scene.instances {
                    M = M_camera * I.transform
                    RenderModel(I.model, M)
                }
            }

        合成相机矩阵与实例变换：M = M_camera * I.transform，
        再交给 render_model 用 M 一次性把顶点变换到相机空间后透视投影。
        相机位于原点、无旋转时 M_camera 为单位矩阵，等价于原先的
        ApplyTransform + ProjectVertex 逐顶点分解式（结果不变）。
        """
        model = instance.model

        # M = M_camera * I.transform（相机矩阵每实例复用，可进一步优化）
        camera_matrix: Matrix4 = self._camera.make_camera_matrix()
        model_matrix: Matrix4 = instance.transform.to_matrix4()
        M: Matrix4 = camera_matrix @ model_matrix

        self.render_model(model, M)

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
