import math

from Color import Color
from Interval import Interval
from Light.AmbientLight import AmbientLight
from Light.DirectionalLight import DirectionalLight
from Light.PointLight import PointLight
from Number import Number
from Point3 import Point3
from Ray import Ray
from Scene import Scene
from Vec3 import Vec3


class RayTracer:
    _scene: Scene

    def __init__(self, scene: Scene):
        self._scene = scene

    def traceRay(self, ray: Ray) -> Color:
        """
        追踪一条射线，返回它"看到的"颜色。

        流程与参考实现保持一致：
        1. 调用 `Scene.closestIntersection` 取最近命中；
        2. 未命中则返回场景背景色；
        3. 命中则求交点 P、法向 N，交给 `compute_lighting` 算光照强度，
           再乘以物体自身颜色。

        Args:
            ray (Ray): 由相机（或反射点）出发的射线。

        Returns:
            Color: 该方向上的最终颜色。
        """

        closest_sphere, closest_t = self._scene.closestIntersection(
            ray,
            Interval(1, math.inf),
        )

        if closest_sphere is None:
            return self._scene.BACKGROUND_COLOR

        point: Point3 = ray.at(closest_t)
        N: Vec3 = (point - closest_sphere.center).normalize()
        # 视线方向 V：由着色点指回相机，即射线方向的反向。
        V: Vec3 = -ray.direction

        return closest_sphere.color * self.compute_lighting(
            point,
            N,
            V,
            closest_sphere.specular,
        )

    def compute_lighting(
            self,
            point: Point3,
            N: Vec3,
            V: Vec3,
            specular: Number,
    ) -> Number:
        """
        计算着色点 p 上的总光照强度（环境光 + 漫反射 + 镜面高光，含阴影）。

        对照参考实现的 ComputeLighting(P, N, V, s)：
        - 环境光直接累加 intensity；
        - 点光源 L = position - P、t_max = 1，平行光 L = direction、t_max = ∞；
        - 先沿 L 做一次阴影检测（ClosestIntersection，从 0.001 起以免自交），
          被遮挡则该光源贡献置零（continue）；
        - 漫反射：intensity * (N·L)，L 为指向光源的单位向量；
        - 镜面高光（Phong）：R = 2 * N * (N·L) - L 为理想反射方向，
          强度取 intensity * (R·V / (|R| * |V|)) ** specular；specular <= 0 时不算高光。
        N 由调用方保证已归一化，故分母 |N| 恒为 1。

        Args:
            point (Point3): 着色点。
            N (Vec3): 该点处已归一化的法向量。
            V (Vec3): 由着色点指向相机的视线方向（无需归一化）。
            specular (Number): 高光指数，<= 0 时不做高光计算。

        Returns:
            Number: 总光照强度，用于乘以物体自身颜色。
        """
        intensity = 0.0

        # V 由调用方保证不是零向量
        V = V.normalize()

        for light in self._scene.lights:

            # 环境光
            if isinstance(light, AmbientLight):
                intensity += light.intensity
                continue

            # 计算指向光源的方向 L，以及阴影检测范围
            if isinstance(light, PointLight):
                L = light.position - point
                t_max: Number = 1

            elif isinstance(light, DirectionalLight):
                L = light.direction
                t_max = math.inf

            else:
                continue

            # 光源恰好位于着色点，无法确定光照方向
            if L.length_squared() == 0:
                continue

            # 阴影检测
            shadow_sphere, _ = self._scene.closestIntersection(
                Ray(point, L),
                Interval(0.001, t_max),
            )

            if shadow_sphere is not None:
                continue

            # 单位化光照方向
            L = L.normalize()

            # N · L
            n_dot_l = N @ L

            # 漫反射
            if n_dot_l > 0:
                intensity += light.intensity * n_dot_l

            # 镜面高光
            if specular > 0:
                R = 2 * N * n_dot_l - L
                r_dot_v = R @ V

                if r_dot_v > 0:
                    intensity += light.intensity * r_dot_v ** specular

        return intensity