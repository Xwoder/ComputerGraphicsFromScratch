"""
2D 栅格化绘制原语，与负责 3D 渲染的 Canvas 完全解耦。

Canvas2D 只承载「直线栅格化」这类 2D 绘制算法，不持有像素缓冲、
也不负责 PPM 输出（那是 3D Canvas 的职责）。这样 3D 渲染管线与
2D 教学示例互不干扰，draw_line 这类原语也能被多个脚本复用。

算法参考 Gabriel Gambetta《Computer Graphics from Scratch》。
"""
from typing import Any

import numpy as np
from Color import Color
from Number import Number
from Point2D import Point2D


class Canvas2D:
    """2D 直线栅格化原语集合（无状态，全部为静态方法）。"""

    @staticmethod
    def interpolate(i0: int,
                    d0: Number,
                    i1: int,
                    d1: Number) -> list[float]:
        """沿 i 从 i0 到 i1 每步 +1，线性插值出对应的 d，返回浮点列表。

        i0 / i1 是插值用的整数索引（直接喂给 range）；d0 / d1 是被插值的
        数值，可以是 int（如坐标 x）也可以是 float（如 draw_shaded_triangle
        里的着色系数 h），故标注为 Number。

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
    def draw_line(p0: Point2D, p1: Point2D) -> list[Point2D]:
        """对称直线栅格化：返回被点亮的栅格单元坐标列表 [(x, y), ...]。

        算法依据 |Δx| 与 |Δy| 选取主轴：
          - 偏水平：x 为主轴，对每个 x 插值出 y；
          - 偏竖直：y 为主轴，对每个 y 插值出 x。
        起点顺序始终保证主轴坐标递增，从而保证采样方向一致。
        """
        cells: list[Point2D] = []
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
                cells.append(Point2D(x, round(ys[x - x0])))
        else:
            # 偏竖直：确保 y 递增
            if a.y > b.y:
                a, b = b, a
            x0, y0 = int(a.x), int(a.y)
            x1, y1 = int(b.x), int(b.y)
            xs = Canvas2D.interpolate(y0, x0, y1, x1)
            for y in range(y0, y1 + 1):
                cells.append(Point2D(round(xs[y - y0]), y))
        return cells

    @staticmethod
    def rasterize_line(k, intercept, x_start, x_end) -> list[Point2D]:
        """朴素栅格化：x 每次递增 1，由 y = kx + b 得到浮点 y，
        再四舍五入到最近的栅格行，每个 x 只点亮一个栅格单元 (x, round(y))。
        作为 draw_line 的对照版本，用于演示无插值画法的失真。"""
        cells: list[Point2D] = []
        x = x_start
        while x <= x_end:
            y = k * x + intercept
            cells.append(Point2D(x, round(y)))  # 最邻近栅格化：每列只点亮一个单元
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
            xl = round(x_left[y - y0])
            xr = round(x_right[y - y0])
            rows.append((y, xl, xr))
        return rows

    @staticmethod
    def draw_filled_triangle(p0: Point2D,
                             p1: Point2D,
                             p2: Point2D) -> set[Point2D]:
        """填充三角形：复用 draw_line 在每条扫描线上画一条水平线段。

        对 fill_triangle_scanlines 返回的每一行 (y, x_left, x_right)，调用
        draw_line((x_left, y), (x_right, y)) 得到该行被点亮的栅格单元，并集后
        即为实心填充——也就是“用画线方法”逐行填满三角形，与线框共用 draw_line。
        """
        cells: set[Point2D] = set()
        for y, xl, xr in Canvas2D.fill_triangle_scanlines(p0, p1, p2):
            cells.update(Canvas2D.draw_line(Point2D(xl, y), Point2D(xr, y)))
        return cells

    def draw_shaded_triangle(self,
                             p0: Point2D,
                             p1: Point2D,
                             p2: Point2D,
                             color: Color,
                             h0: float,
                             h1: float,
                             h2: float,
                             alpha: float = 1.0) -> None:
        """带插值着色的三角形（Shaded Triangle）。

        对应 Gabriel Gambetta《Computer Graphics from Scratch》中的
        DrawShadedTriangle(P0, P1, P2, color)：每个顶点带一个 h 着色系数
        （通常 0~1），三角形内部每个像素的着色系数由顶点 h 先沿三条边、再沿
        每条水平扫描线两次线性插值得到，最终颜色 = color * h_pixel。

        算法步骤（标注 ❶~❹ 与书中一致）：
          ❶ 三个顶点按 y 升序排序，使 y0 <= y1 <= y2（h 随点同步交换）。
          ❷ 沿 y 插值三条边的 x 与 h（x01/h01、x12/h12、x02/h02）。
          ❸ 去掉 x01/h01 末项（与 x12/h12 首行重复）拼接成 x012/h012；
             取中点比较 x02 与 x012，判定左 / 右边界。
          ❹ 逐条扫描线：对每行左右端点再做一次 h 的水平插值，
             遍历 [x_l, x_r] 每个像素写 color * h。
        """
        # 端点先吸附到最近整数栅格（与 draw_line 语义一致）
        a: Point2D = Point2D(round(p0.x), round(p0.y))
        b: Point2D = Point2D(round(p1.x), round(p1.y))
        c: Point2D = Point2D(round(p2.x), round(p2.y))

        # ❶ 按 y 升序排序，并同步带着各自的 h 值一起交换（保证 y0 <= y1 <= y2）
        pts = [a, b, c]
        hs = [h0, h1, h2]
        if pts[1].y < pts[0].y:
            pts[0], pts[1] = pts[1], pts[0]
            hs[0], hs[1] = hs[1], hs[0]
        if pts[2].y < pts[0].y:
            pts[0], pts[2] = pts[2], pts[0]
            hs[0], hs[2] = hs[2], hs[0]
        if pts[2].y < pts[1].y:
            pts[1], pts[2] = pts[2], pts[1]
            hs[1], hs[2] = hs[2], hs[1]

        P0, P1, P2 = pts
        x0, y0 = int(P0.x), int(P0.y)
        x1, y1 = int(P1.x), int(P1.y)
        x2, y2 = int(P2.x), int(P2.y)
        h0, h1, h2 = hs

        # ❷ 沿 y 插值三条边的 x 与 h
        x01 = Canvas2D.interpolate(y0, x0, y1, x1)
        h01 = Canvas2D.interpolate(y0, h0, y1, h1)
        x12 = Canvas2D.interpolate(y1, x1, y2, x2)
        h12 = Canvas2D.interpolate(y1, h1, y2, h2)
        x02 = Canvas2D.interpolate(y0, x0, y2, x2)
        h02 = Canvas2D.interpolate(y0, h0, y2, h2)

        # ❸ 去掉两条短边的末项再拼接，避免 y1 行重复；取中点判定左 / 右边界
        x01.pop()
        h01.pop()
        x012 = x01 + x12
        h012 = h01 + h12

        m = len(x012) // 2
        if x02[m] < x012[m]:
            x_left, x_right = x02, x012
            h_left, h_right = h02, h012
        else:
            x_left, x_right = x012, x02
            h_left, h_right = h012, h02

        # ❹ 逐条扫描线：水平方向再插值一次 h，逐像素着色
        for y in range(y0, y2 + 1):
            x_l = round(x_left[y - y0])
            x_r = round(x_right[y - y0])
            h_segment = Canvas2D.interpolate(x_l, h_left[y - y0], x_r, h_right[y - y0])
            for x in range(x_l, x_r + 1):
                h = h_segment[x - x_l]
                shaded = color * h          # Color.__mul__ 已做 0~255 钳制
                self.putPixel(x, y, (shaded.red / 255.0,
                                     shaded.green / 255.0,
                                     shaded.blue / 255.0,
                                     alpha))

    def __init__(self, width: int, height: int,
                 background: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)):
        """创建一个 width×height 的 2D 帧缓冲（RGBA 浮点数组）。

        与 3D 的 Canvas 不同，这里仅持有一个像素缓冲，不负责 PPM 输出
        （那是 3D Canvas 的职责）；渲染交给上层（如 matplotlib.imshow）。
        """
        self.width = width
        self.height = height
        self.buffer = np.zeros((height, width, 4), dtype=float)
        self.buffer[:] = background

    def putPixel(self, x: float, y: float,
                 color: tuple[float, float, float, float]) -> None:
        """在帧缓冲 (x, y) 处点亮一个颜色为 color 的栅格单元。

        color 为 (r, g, b, a)（各分量 0~1）；坐标先 round 吸附到最近整数
        栅格，越界则忽略。这是 3D Canvas.putPixel 的 2D 对应版本，使
        上层（如三角形绘制）可以逐格写入带颜色的像素。
        """
        xi = round(x)
        yi = round(y)
        if 0 <= xi < self.width and 0 <= yi < self.height:
            self.buffer[yi, xi] = color

    def Clear(self, background: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)) -> None:
        """把整个帧缓冲重置为 background。"""
        self.buffer[:] = background

    def as_array(self):
        """返回 RGBA 帧缓冲（shape=(height, width, 4)），供 imshow 等渲染。"""
        return self.buffer
