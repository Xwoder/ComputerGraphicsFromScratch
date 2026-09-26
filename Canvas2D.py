"""
2D 栅格化绘制原语，与负责 3D 渲染的 Canvas 完全解耦。

Canvas2D 只承载「直线栅格化」这类 2D 绘制算法，不持有像素缓冲、
也不负责 PPM 输出（那是 3D Canvas 的职责）。这样 3D 渲染管线与
2D 教学示例互不干扰，draw_line 这类原语也能被多个脚本复用。

算法参考 Gabriel Gambetta《Computer Graphics from Scratch》。
"""

from Point2 import Point2


class Canvas2D:
    """2D 直线栅格化原语集合（无状态，全部为静态方法）。"""

    @staticmethod
    def interpolate(i0, d0, i1, d1):
        """沿 i 从 i0 到 i1 每步 +1，线性插值出对应的 d，返回浮点列表。

        返回长度 = |i1 - i0| + 1，列表第 k 个值对应 i = i0 + k。
        当 i0 == i1 时退化为仅含 d0 的单元素列表。
        """
        if i0 == i1:
            return [d0]
        values = []
        a = (d1 - d0) / (i1 - i0)  # 每步增量
        d = d0
        for i in range(i0, i1 + 1):
            values.append(d)
            d = d + a
        return values

    @staticmethod
    def draw_line(p0: Point2, p1: Point2):
        """对称直线栅格化：返回被点亮的栅格单元坐标列表 [(x, y), ...]。

        算法依据 |Δx| 与 |Δy| 选取主轴：
          - 偏水平：x 为主轴，对每个 x 插值出 y；
          - 偏竖直：y 为主轴，对每个 y 插值出 x。
        起点顺序始终保证主轴坐标递增，从而保证采样方向一致。
        """
        cells = []
        # 栅格坐标必须为整数：端点先吸附到最近的栅格单元（round），
        # 与数据轴 int(round(...)) 的语义保持一致；int() 会向零截断，
        # 对 99.4/98.7 这类浮点端点会造成线段少画、落错格子。
        x0, y0 = round(p0.x), round(p0.y)
        x1, y1 = round(p1.x), round(p1.y)

        if abs(x1 - x0) > abs(y1 - y0):
            # 偏水平：确保 x 递增
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            ys = Canvas2D.interpolate(x0, y0, x1, y1)
            for x in range(x0, x1 + 1):
                cells.append((x, int(round(ys[x - x0]))))
        else:
            # 偏竖直：确保 y 递增
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
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
