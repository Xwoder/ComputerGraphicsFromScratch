"""
使用 Pillow 以栅格画法绘制直线。

设计要点：
  1. 起始点 A = (0, 1)，三条直线均过该点，截距 b = 1。
  2. 用斜截式 y = kx + b 表示直线，斜率 k 与截距 b 直接给定。
  3. x 每次只递增 1 个栅格单位（一个“点”），由 y = kx + b 得到浮点 y，
     再把 y 四舍五入到最近的栅格行——即每次只“点亮”一个栅格单元（最邻近栅格化）。
  4. 使用 Pillow 把被点亮的栅格单元（实心方格）画在 100×100 栅格上，
     并用淡色连续直线作为“理想直线”参考，便于对比栅格化误差。
  5. 绘制结果同时保存为 graph_line_no_interpolation.png。
  （刻度与坐标标注较复杂，此处先不绘制。）
"""

from PIL import Image, ImageDraw

from Canvas2D import Canvas2D
from Point2D import Point2D

# 每个栅格单元对应的像素边长
SCALE = 8
GRID = 100
W, H = GRID * SCALE, GRID * SCALE


def grid_to_image(x: int, y: int) -> tuple[int, int, int, int]:
    """把栅格单元 (x, y) 映射成图像中的像素矩形 (left, top, right, bottom)。

    Pillow 图像原点在左上、y 轴向下，而网格 y 轴向上，故按 (GRID - y - 1) 翻转。
    """
    left = x * SCALE
    top = (GRID - y - 1) * SCALE
    return left, top, left + SCALE, top + SCALE


def point_to_image(p: Point2D) -> tuple[float, float]:
    """把网格坐标点映射成图像坐标（用于绘制理想直线）。"""
    return p.x * SCALE, (GRID - p.y) * SCALE


def main():
    A = Point2D(0, 1)  # 三条直线的公共起始点 (0,1)

    # 要绘制的多条直线：(终点 P1, 颜色, 图例名)
    # 起点统一为 A=(0,1)，由 A 与 P1 反推斜率 k 与截距 b。
    # 颜色用 (R, G, B) 表示，对应原 Matplotlib 的 tab:red / tab:orange / tab:green。
    LINES = [
        (Point2D(90, 46), (255, 45, 85), r"y = (1/2)x + 1"),
        (Point2D(98, 99), (255, 153, 51), "y = x + 1"),
        (Point2D(32, 97), (44, 170, 80), "y = 3x + 1"),
    ]

    print("=" * 60)
    print(f"起始点 A = {A}，各直线截距 b = 1（均过 (0,1)）")
    print("=" * 60)

    # 白色背景的 RGBA 画布
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    for p1, color, name in LINES:
        # 由 A 与 p1 反推斜截式 y = kx + b
        k = (p1.y - A.y) / (p1.x - A.x)
        b = A.y - k * A.x
        x_end = p1.x

        # 理想直线（淡色连续，作为栅格化的参考）
        ax0, ay0 = point_to_image(A)
        ax1, ay1 = point_to_image(p1)
        draw.line([(ax0, ay0), (ax1, ay1)],
                  fill=(color[0], color[1], color[2], int(0.4 * 255)),
                  width=2)

        # 栅格画法：每列只点亮一个最近的栅格单元（仅保留落在 100×100 内的）
        cells = Canvas2D.rasterize_line(k, b, A.x, x_end)
        for c in cells:
            if 0 <= c.y < GRID:
                rect = grid_to_image(int(c.x), int(c.y))
                draw.rectangle(rect,
                               fill=(color[0], color[1], color[2], int(0.85 * 255)))

    # 保存为 PNG 图片
    img.save("graph_line_no_interpolation.png")
    print("已保存： graph_line_no_interpolation.png")


if __name__ == "__main__":
    main()
