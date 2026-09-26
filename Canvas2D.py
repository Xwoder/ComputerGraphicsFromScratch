"""
2D 栅格化绘制原语，与负责 3D 渲染的 Canvas 完全解耦。

Canvas2D 只承载「直线栅格化」这类 2D 绘制算法，不持有像素缓冲、
也不负责 PPM 输出（那是 3D Canvas 的职责）。这样 3D 渲染管线与
2D 教学示例互不干扰，draw_line 这类原语也能被多个脚本复用。

算法参考 Gabriel Gambetta《Computer Graphics from Scratch》。
"""
from typing import Any

from Number import Number
from Point2D import Point2D


class Canvas2D:
    """2D 直线栅格化原语集合（无状态，全部为静态方法）。"""

    @staticmethod
    def interpolate(i0: int,
                    d0: int,
                    i1: int,
                    d1: int) -> list[float]:
        """沿 i 从 i0 到 i1 每步 +1，线性插值出对应的 d，返回浮点列表。

        返回长度 = |i1 - i0| + 1，列表第 k 个值对应 i = i0 + k。
        当 i0 == i1 时退化为仅含 d0 的单元素列表。
        """
        if i0 == i1:
            return [float(d0)]
        values: list[float] = []
        a: float = (d1 - d0) / (i1 - i0)  # 每步增量
        d: float = d0
        for i in range(i0, i1 + 1):
            values.append(d)
            d = d + a
        return values

    @staticmethod
    def draw_line(p0: Point2D, p1: Point2D):
        """对称直线栅格化：返回被点亮的栅格单元坐标列表 [(x, y), ...]。

        算法依据 |Δx| 与 |Δy| 选取主轴：
          - 偏水平：x 为主轴，对每个 x 插值出 y；
          - 偏竖直：y 为主轴，对每个 y 插值出 x。
        起点顺序始终保证主轴坐标递增，从而保证采样方向一致。
        """
        cells: list[tuple[int, int]] = []
        # 栅格坐标必须为整数：端点先吸附到最近的栅格单元（round），
        # 并用 Point2D 封装 (x, y)。交换端点时用 Point2D 整体交换
        # （a, b = b, a），比四元组交换 x0,y0,x1,y1 更清晰、不会把 x/y 配对弄错。
        # 注意 Point2D.x 标注为 Number，故交换后再显式转 int 供 range/下标使用
        # （int() 会向零截断，对 99.4/98.7 这类浮点端点会造成线段少画、落错格子）。
        a: Point2D = Point2D(round(p0.x), round(p0.y))
        b: Point2D = Point2D(round(p1.x), round(p1.y))

        if abs(b.x - a.x) > abs(b.y - a.y):
            # 偏水平：确保 x 递增
            if a.x > b.x:
                a, b = b, a
            x0, y0 = int(a.x), int(a.y)
            x1, y1 = int(b.x), int(b.y)
            ys = Canvas2D.interpolate(x0, y0, x1, y1)
            for x in range(x0, x1 + 1):
                cells.append((x, int(round(ys[x - x0]))))
        else:
            # 偏竖直：确保 y 递增
            if a.y > b.y:
                a, b = b, a
            x0, y0 = int(a.x), int(a.y)
            x1, y1 = int(b.x), int(b.y)
            xs = Canvas2D.interpolate(y0, x0, y1, x1)
            for y in range(y0, y1 + 1):
                cells.append((int(round(xs[y - y0])), y))
        return cells

    @staticmethod
    def rasterize_line(k, intercept, x_start, x_end):
        """朴素栅格化：x 每次递增 1，由 y = kx + b 得到浮点 y，
        再四舍五入到最近的栅格行，每个 x 只点亮一个栅格单元 (x, round(y))。
        作为 draw_line 的对照版本，用于演示无插值画法的失真。"""
        cells = []
        x = x_start
        while x <= x_end:
            y = k * x + intercept
            cells.append((x, int(round(y))))  # 最邻近栅格化：每列只点亮一个单元
            x += 1
        return cells

    @staticmethod
    def fill_triangle_scanlines(p0: Point2D,
                                p1: Point2D,
                                p2: Point2D) -> list[tuple[int, int, int]]:
        """三角形填充的扫描线：返回每一行的 (y, x_left, x_right)。

        对应 Gabriel Gambetta 的 DrawFilledTriangle 思路：按 y 升序排序后沿
        扫描线插值三条边的 x 坐标，比较中点判定左/右边界，得到每条扫描线在 y
        处的左右端点 x。返回的每行 (y, x_left, x_right) 可直接交给 draw_line
        连成一条水平线段——“用画线的方法”逐行填满三角形。

        返回：list of (y, xl, xr)，y 从最小到最大递增。
        """
        # ❶ 端点先吸附到最近整数栅格（与 draw_line 语义一致），再按 y 升序排序
        a: Point2D = Point2D(round(p0.x), round(p0.y))
        b: Point2D = Point2D(round(p1.x), round(p1.y))
        c: Point2D = Point2D(round(p2.x), round(p2.y))
        if b.y < a.y:
            a, b = b, a
        if c.y < a.y:
            a, c = c, a
        if c.y < b.y:
            b, c = c, b
        x0, y0 = int(a.x), int(a.y)
        x1, y1 = int(b.x), int(b.y)
        x2, y2 = int(c.x), int(c.y)

        # ❷ 沿 y 插值每条边的 x 坐标（interpolate(i0, d0, i1, d1)：i 取 y，d 取 x）
        x01: list[float] = Canvas2D.interpolate(y0, x0, y1, x1)
        x12: list[float] = Canvas2D.interpolate(y1, x1, y2, x2)
        x02: list[float] = Canvas2D.interpolate(y0, x0, y2, x2)

        # ❸ 去掉 x01 末项（y1 处与 x12 首项重复），拼接两条短边
        x01.pop()
        x012 = x01 + x12

        # ❹ 比较中点，判定左 / 右边界
        m = len(x012) // 2
        if x02[m] < x012[m]:
            x_left, x_right = x02, x012
        else:
            x_left, x_right = x012, x02

        # ❺ 逐条扫描线记录左右端点（四舍五入吸附到栅格列）
        rows: list[tuple[int, int, int]] = []
        for y in range(y0, y2 + 1):
            xl = int(round(x_left[y - y0]))
            xr = int(round(x_right[y - y0]))
            rows.append((y, xl, xr))
        return rows

    @staticmethod
    def draw_filled_triangle(p0: Point2D,
                             p1: Point2D,
                             p2: Point2D) -> set[tuple[int, int]]:
        """填充三角形：复用 draw_line 在每条扫描线上画一条水平线段。

        对 fill_triangle_scanlines 返回的每一行 (y, x_left, x_right)，调用
        draw_line((x_left, y), (x_right, y)) 得到该行被点亮的栅格单元，并集后
        即为实心填充——也就是“用画线方法”逐行填满三角形，与线框共用 draw_line。
        """
        cells: set[tuple[int, int]] = set()
        for y, xl, xr in Canvas2D.fill_triangle_scanlines(p0, p1, p2):
            cells.update(Canvas2D.draw_line(Point2D(xl, y), Point2D(xr, y)))
        return cells
