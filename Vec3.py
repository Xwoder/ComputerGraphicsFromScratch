import math
from dataclasses import dataclass

from Number import Number


@dataclass(frozen=True)
class Vec3:
    x: Number = 0
    y: Number = 0
    z: Number = 0

    def __neg__(self) -> Vec3:
        """
        一元负号运算符（-v），返回各分量取反的新向量。
        对应 C++ 的 vec3 operator-() const。
        """
        return Vec3(-self.x, -self.y, -self.z)

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
        if not 0 <= i <= 2:
            raise IndexError("Vec3 index out of range")
        return (self.x, self.y, self.z)[i]

    def __add__(self, other: Vec3) -> Vec3:
        """
        向量加法（v + u），返回新向量（对应 C++ 的 operator+）。
        不修改原向量。
        """
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        """
        向量减法（v - u），返回新向量（对应 C++ 的 operator-）。
        不修改原向量。
        """
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: "Vec3 | Number") -> Vec3:
        """
        乘法（v * t 或 v * u），返回新向量，不修改原向量。
        - 标量 t：各分量乘以 t（对应 C++ 的 operator*(double)）。
        - 向量 u：逐分量相乘（Hadamard 积）。
        """
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: "Number") -> Vec3:
        """
        右乘（t * v），使标量可写在左侧。直接复用 __mul__。
        """
        return self.__mul__(other)

    def __truediv__(self, other: "Vec3 | Number") -> Vec3:
        """
        除法（v / t 或 v / u），返回新向量，不修改原向量。
        - 标量 t：各分量除以 t（对应 C++ 的 operator/(double)）。
        - 向量 u：逐分量相除。
        """
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __matmul__(self, other: Vec3) -> Number:
        return (
                self.x * other.x
                + self.y * other.y
                + self.z * other.z
        )

    def __eq__(self, other: object) -> bool:
        """
        相等判断（v == u），当三个分量都相等时返回 True。
        若 other 不是 Vec3，则返回 NotImplemented 交由 Python 处理。
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self) -> str:
        """
        返回向量的官方字符串表示，形如 Vec3(x, y, z)。
        供 repr()、交互式解释器及调试使用。
        """
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def length_squared(self) -> float:
        """
        计算向量长度的平方（模的平方），即 x² + y² + z²。
        对应 C++ 的 length_squared()。
        """
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def length(self) -> float:
        """
        计算向量的欧几里得长度（模），即 sqrt(length_squared())。
        对应 C++ 的 length()。
        """
        return math.sqrt(self.length_squared())

    def dot(self, other: Vec3) -> Number:
        """
        向量内积（点积），返回标量。
        对应 C++ 的 dot(const vec3&, const vec3&)。
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self) -> Vec3:
        return self / self.length()