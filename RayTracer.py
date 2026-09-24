import math

from Color import Color
from Interval import Interval
from Light.AmbientLight import AmbientLight
from Light.Light import Light
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
            self._scene.lights
        )

    @staticmethod
    def compute_lighting(
            point: Point3,
            N: Vec3,
            V: Vec3,
            specular: Number,
            lights: list[Light],
    ) -> Number:
        """
        计算着色点 p 上的总光照强度（漫反射 + 镜面高光）。

        漫反射：intensity * (N·L)，L 为指向光源的单位向量。
        镜面高光（Phong）：R = 2 * N * (N·L) - L 为理想反射方向，
        强度取 intensity * (R·V / (|R| * |V|)) ** specular，即 cos(alpha) 的
        specular 次方；指数越大高光越锐利，specular <= 0 表示无高光。

        Args:
            point (Point3): 着色点。
            N (Vec3): 该点处已归一化的法向量。
            V (Vec3): 由着色点指向相机的视线方向（无需归一化）。
            specular (Number): 高光指数，<= 0 时不做高光计算。
            lights (list[Light]): 场景中的光源列表。

        Returns:
            Number: 总光照强度，用于乘以物体自身颜色。
        """

        # N 由调用方保证已归一化（traceRay），分母中的 |N| 恒为 1，无需再除。
        # 每个光源只需把光方向归一化一次，即可直接用点积得到 cos(theta)。
        intensity = 0.0

        for light in lights:

            if isinstance(light, AmbientLight):
                intensity += light.intensity
                continue
            else:
                direction: Vec3 = light.get_direction(point)

                # 退化情形：点光源恰好落在着色点上，方向为零向量，无法归一化
                if direction.length_squared() == 0:
                    continue

                L: Vec3 = direction.normalize()

                l_dot_n: Number = L.dot(N)

                if l_dot_n > 0:
                    intensity += light.intensity * l_dot_n

                # 高光项独立于漫反射项：只要反射方向偏向视线就贡献亮度。
                if specular > 0:
                    R: Vec3 = (2 * N * l_dot_n - L).normalize()
                    r_dot_v: Number = R.dot(V.normalize())

                    if r_dot_v > 0:
                        intensity += light.intensity * r_dot_v ** specular

        return intensity
