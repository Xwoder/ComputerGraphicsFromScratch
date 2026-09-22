import math
from typing import Sequence

from Number import Number


class Vec3:
    _x: Number
    _y: Number
    _z: Number

    def __init__(self,
                 x: Number = 0,
                 y: Number = 0,
                 z: Number = 0):
        """
        初始化三维向量，使用给定的三个分量设置 x、y、z 坐标。

        Args:
            x (Number): x 轴方向的分量，取值类型为 float 或 int。
            y (Number): y 轴方向的分量，取值类型为 float 或 int。
            z (Number): z 轴方向的分量，取值类型为 float 或 int。
        """

        self._x = x
        self._y = y
        self._z = z

    @classmethod
    def from_sequence(cls, value: Sequence[Number]):
        """
        从包含三个分量的序列构造 Vec3 实例

        Args:
            value (Sequence[Number]): 包含三个数值分量的序列（如列表或元组）

        Returns:
            Vec3: 由序列中三个分量依次作为 x、y、z 构造的向量实例

        Raises:
            ValueError: 当序列长度不等于 3 时抛出
        """

        if len(value) != 3:
            raise ValueError("Vec3 requires exactly 3 values")

        x = value[0]
        y = value[1]
        z = value[2]

        return cls(x, y, z)

    @property
    def x(self) -> Number:
        """
        向量的 x 分量（只读属性）。

        Returns:
            Number: x 轴方向的分量
        """
        return self._x

    @property
    def y(self) -> Number:
        """
        向量的 y 分量（只读属性）。

        Returns:
            Number: y 轴方向的分量
        """
        return self._y

    @property
    def z(self) -> Number:
        """
        向量的 z 分量（只读属性）。

        Returns:
            Number: z 轴方向的分量
        """
        return self._z

    def __neg__(self) -> "Vec3":
        """
        一元负号运算符（-v），返回各分量取反的新向量。
        对应 C++ 的 vec3 operator-() const。

        Returns:
            Vec3: 各分量取反后的新向量
        """
        return Vec3(-self._x, -self._y, -self._z)

    def __getitem__(self, i: int) -> Number:
        """
        下标访问运算符（v[i]），返回第 i 个分量。
        对应 C++ 的 double operator[](int i) const。

        Args:
            i (int): 分量索引，0 表示 x，1 表示 y，2 表示 z。

        Returns:
            Number: 对应的分量值

        Raises:
            IndexError: 当索引不在 0~2 范围内时抛出
        """
        if i == 0:
            return self._x
        if i == 1:
            return self._y
        if i == 2:
            return self._z
        raise IndexError("Vec3 index out of range")

    def __add__(self, other: "Vec3") -> Vec3:
        """
        向量加法（v + u），返回新向量（对应 C++ 的 operator+）。
        不修改原向量。

        Args:
            other (Vec3): 被加的向量。

        Returns:
            Vec3: 分量相加后的新向量
        """
        return Vec3(self._x + other.x, self._y + other.y, self._z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        """
        向量减法（v - u），返回新向量（对应 C++ 的 operator-）。
        不修改原向量。

        Args:
            other (Vec3): 被减的向量。

        Returns:
            Vec3: 分量相减后的新向量
        """
        return Vec3(self._x - other.x, self._y - other.y, self._z - other.z)

    def __mul__(self, other: "Vec3 | Number") -> Vec3:
        """
        乘法（v * t 或 v * u），返回新向量，不修改原向量。
        - 标量 t：各分量乘以 t（对应 C++ 的 operator*(double)）。
        - 向量 u：逐分量相乘（Hadamard 积）。

        Args:
            other (Vec3 | Number): 右侧操作数，可为标量或向量。

        Returns:
            Vec3: 相乘后的新向量
        """
        if isinstance(other, Vec3):
            return Vec3(self._x * other.x, self._y * other.y, self._z * other.z)
        return Vec3(self._x * other, self._y * other, self._z * other)

    def __rmul__(self, other: "Number") -> Vec3:
        """
        右乘（t * v），使标量可写在左侧。直接复用 __mul__。

        Args:
            other (Number): 左侧的标量。

        Returns:
            Vec3: 相乘后的新向量
        """
        return self.__mul__(other)

    def __truediv__(self, other: "Vec3 | Number") -> Vec3:
        """
        除法（v / t 或 v / u），返回新向量，不修改原向量。
        - 标量 t：各分量除以 t（对应 C++ 的 operator/(double)）。
        - 向量 u：逐分量相除。

        Args:
            other (Vec3 | Number): 右侧操作数，可为标量或向量。

        Returns:
            Vec3: 相除后的新向量
        """
        if isinstance(other, Vec3):
            return Vec3(self._x / other.x, self._y / other.y, self._z / other.z)
        return Vec3(self._x / other, self._y / other, self._z / other)

    def __eq__(self, other: object) -> bool:
        """
        相等判断（v == u），当三个分量都相等时返回 True。
        对应 C++ 的 operator==。若 other 不是 Vec3，则返回 NotImplemented
        交由 Python 处理（通常得到 False）。

        Args:
            other (object): 比较对象。

        Returns:
            bool: 分量是否全部相等
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return self._x == other.x and self._y == other.y and self._z == other.z

    def length_squared(self) -> float:
        """
        计算向量长度的平方（模的平方），即 x² + y² + z²。
        对应 C++ 的 length_squared()。

        Returns:
            float: 各分量平方和
        """
        return self._x ** 2 + self._y ** 2 + self._z ** 2

    def near_zero(self) -> bool:
        """
        判断向量是否在各个分量上都接近零（用于剔除散射方向上的退化/噪声向量）。
        对应 C++ 的 near_zero()。

        Returns:
            bool: 当 x、y、z 三个分量的绝对值都小于 1e-8 时返回 True
        """
        s: Number = 1e-8
        return abs(self._x) < s and abs(self._y) < s and abs(self._z) < s

    def length(self) -> float:
        """
        计算向量的欧几里得长度（模），即 sqrt(length_squared())。
        对应 C++ 的 length()（内部委托给 length_squared()）。

        Returns:
            float: 向量各分量平方和的算术平方根
        """
        return math.sqrt(self.length_squared())

    def dot(self, other: Vec3) -> Number:
        """
        向量内积（点积），返回标量。
        对应 C++ 的 dot(const vec3&, const vec3&)。

        Args:
            other (Vec3): 另一个向量。

        Returns:
            Number: 各分量乘积之和（x1*x2 + y1*y2 + z1*z2）
        """
        return self._x * other.x + self._y * other.y + self._z * other.z

    def unit_vector(self) -> Vec3:
        """
        返回当前向量的单位向量（方向相同、长度为 1）。
        实现为 self / self.length()，不修改原向量（对应 C++ 的 unit_vector）。
        注意：若向量长度为零，将触发除零错误（ZeroDivisionError）。

        Returns:
            Vec3: 归一化后的新向量
        """
        return self / self.length()

    def __repr__(self) -> str:
        """
        返回向量的官方字符串表示，形如 Vec3(x, y, z)。
        供 repr()、交互式解释器及调试使用；其输出应满足 eval(repr(v))
        可还原出等价对象。

        Returns:
            str: 包含三个分量的字符串表示
        """
        return f"Vec3({self._x}, {self._y}, {self._z})"

    def cross(self, other: Vec3) -> Vec3:
        """
        向量叉积（外积），返回一个与 self 和 other 都垂直的新向量。
        对应 C++ 的 cross(const vec3&, const vec3&)。
        结果方向由右手定则确定，长度等于 |self| * |other| * sin(theta)
        （即两向量张成平行四边形的面积）。

        Args:
            other (Vec3): 另一个向量。

        Returns:
            Vec3: 叉积得到的新向量
        """
        return Vec3(
            self._y * other.z - self._z * other.y,
            self._z * other.x - self._x * other.z,
            self._x * other.y - self._y * other.x,
        )

    @staticmethod
    def reflect(v: Vec3, n: Vec3) -> Vec3:
        """
        向量反射：计算 v 关于法线 n 的镜面反射方向。
        对应 C++ 的 inline vec3 reflect(const vec3& v, const vec3& n) {
            return v - 2*dot(v,n)*n;
        }
        n 必须是单位向量；结果长度与 v 相同，方向满足入射角等于反射角。

        Args:
            v (Vec3): 入射方向向量（通常指向表面）。
            n (Vec3): 单位法线向量。

        Returns:
            Vec3: 反射方向向量 v - 2*dot(v,n)*n
        """
        return v - 2 * v.dot(n) * n

    @staticmethod
    def refract(uv: Vec3, n: Vec3, etai_over_etat: Number) -> Vec3:
        """
        向量折射：计算方向 uv 穿过法线 n 分界面时的折射方向。
        对应 C++ 的 inline vec3 refract(const vec3& uv, const vec3& n,
        double etai_over_etat)。

            auto cos_theta = std::fmin(dot(-uv, n), 1.0);
            vec3 r_out_perp =  etai_over_etat * (uv + cos_theta*n);
            vec3 r_out_parallel = -std::sqrt(std::fabs(1.0 - r_out_perp.length_squared())) * n;
            return r_out_perp + r_out_parallel;

        uv 与 n 均应为单位向量。etai_over_etat 为相对折射率（入射介质折射率
        / 折射介质折射率）。r_out_perp 为折射方向垂直于法线的分量，
        r_out_parallel 为平行于法线的分量（取负号使光线弯向法线一侧）。
        cos_theta 用 std::fmin 钳制到 [.., 1.0] 以避免数值误差导致的越界。

        Args:
            uv (Vec3): 入射单位方向向量（指向表面）。
            n (Vec3): 单位法线向量。
            etai_over_etat (Number): 相对折射率 etai/etat。

        Returns:
            Vec3: 折射后的单位方向向量（按公式直接相加，未强制归一化）。
        """
        cos_theta = min(-uv.dot(n), 1.0)
        r_out_perp = etai_over_etat * (uv + cos_theta * n)
        r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel

    @classmethod
    def zero(cls) -> Vec3:
        return cls(0, 0, 0)

    @classmethod
    def one(cls) -> Vec3:
        return cls(1, 1, 1)

    @classmethod
    def random(cls,
               min: Number = 0.0,
               max: Number = 1.0) -> Vec3:
        """
        返回一个各分量均为独立随机实数的向量。

        对应 C++ vec3 的两个静态重载：
            static vec3 random();                        // 各分量取 [0,1)
            static vec3 random(double min, double max);  // 各分量取 [min,max)
        Python 里用默认参数合并为一个：不传参即 [0,1)，传入区间即 [min,max)。

        Args:
            min (Number): 分量下界（含），默认 0.0。
            max (Number): 分量上界（不含），默认 1.0。

        Returns:
            Vec3: 三个分量各自独立随机的新向量。
        """
        # 延迟导入：Random 依赖 Vec3，若在模块顶层导入会形成循环导入
        from Random import random_number

        return cls(
            random_number(min, max),
            random_number(min, max),
            random_number(min, max),
        )

    @classmethod
    def random_unit_vector(cls) -> Vec3:
        """
        返回一个随机单位向量（方向均匀分布在单位球面上）。

        对应 C++ vec3.h 中的 inline 函数：
            inline vec3 random_unit_vector() {
                while (true) {
                    auto p = vec3::random(-1,1);
                    auto lensq = p.length_squared();
                    if (1e-160 < lensq && lensq <= 1)
                        return p / sqrt(lensq);
                }
            }

        做法是在 [-1,1]³ 立方体内随机取点，只接受落在单位球内（1e-160 <
        |p|² <= 1）的点再归一化——即拒绝采样。下界 1e-160 用于排除长度过小
        （尤其是零向量）导致的数值问题。立方体体积 8、球体积 4π/3，
        接受率约 52%，循环期望执行约 2 次。

        Returns:
            Vec3: 长度为 1 的随机方向向量。
        """
        while True:
            p: Vec3 = cls.random(-1, 1)
            lensq: float = p.length_squared()
            # 排除长度过小（含零向量）与球外（含退化）的点
            if 1e-160 < lensq <= 1:
                unit_vector: Vec3 = p / math.sqrt(lensq)
                return unit_vector

    @classmethod
    def random_on_hemisphere(cls, normal: Vec3) -> Vec3:
        """
        返回一个随机单位向量，且保证它落在 normal 所在的那一侧半球。

        对应 C++ vec3.h 中的 inline 函数：
            inline vec3 random_on_hemisphere(const vec3& normal) {
                vec3 on_unit_sphere = random_unit_vector();
                if (dot(on_unit_sphere, normal) > 0.0) // 与法线同半球
                    return on_unit_sphere;
                else
                    return -on_unit_sphere;
            }

        做法很直接：先取一个随机单位向量，若它与 normal 的点积为负（说明落在
        另一侧半球），就整体取反翻回来。结果仍是单位向量，且
        dot(结果, normal) > 0。normal 只需指明方向，不必是单位长度。

        Args:
            normal (Vec3): 半球的方向（通常是命中点处的表面法线）。

        Returns:
            Vec3: 长度为 1、且与 normal 同侧的随机方向向量。
        """
        on_unit_sphere: Vec3 = cls.random_unit_vector()
        # 与法线同半球（点积为正）则保留，否则翻到法线这一侧
        if on_unit_sphere.dot(normal) > 0.0:
            return on_unit_sphere
        else:
            return -on_unit_sphere

    @classmethod
    def random_in_unit_disk(cls) -> Vec3:
        """
        返回一个单位圆盘（z=0 平面、半径 1）内均匀分布的随机向量。

        对应 C++ vec3.h 中的 inline 函数：
            inline vec3 random_in_unit_disk() {
                while (true) {
                    auto p = vec3(random_double(-1,1), random_double(-1,1), 0);
                    if (p.length_squared() < 1)
                        return p;
                }
            }

        做法：在 [-1,1]×[-1,1] 的正方形内随机取点（z 固定为 0），只接受到原点
        距离平方小于 1（即落在单位圆盘内）的点——拒绝采样。正方形面积 4、
        圆盘面积 π，接受率约 78.5%。结果 z 分量恒为 0，且长度 < 1。

        Returns:
            Vec3: 落在单位圆盘内（距原点 < 1）的随机向量，z = 0。
        """
        # 延迟导入：Random 依赖 Vec3，若在模块顶层导入会形成循环导入
        from Random import random_number

        while True:
            p: Vec3 = cls(random_number(-1, 1), random_number(-1, 1), 0)
            if p.length_squared() < 1:
                return p
