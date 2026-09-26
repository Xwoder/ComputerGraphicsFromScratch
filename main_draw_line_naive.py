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
  （坐标轴、刻度与标题复用 plot_utils，与三角形脚本同一套布局。）
"""

from PIL import Image, ImageDraw

from Canvas2D import Canvas2D
from Color import Color
from ImageViewer import ImageViewer
from LineByTwoPoints import LineByTwoPoints
from Point2D import Point2D
from plot_utils import (GRID, W, H, cell_rect, point_to_image, draw_grid,
                        draw_ticks_and_labels, load_font)


def main():
    startPoint: Point2D = Point2D(0, 1)  # 三条直线的公共起始点 (0,1)

    # 要绘制的多条直线：用 Line 封装起点/终点/颜色/名称。
    # 每条线显式保存自己的 start 与 end。当前起点都取 startPoint=(0,1)（均过 (0,1)），
    # 但结构上已允许后续各线段使用不同的起点，无需改动循环。
    # 颜色用 Color（RGB 0~255）表示，对应原 Matplotlib 的 tab:red / tab:orange / tab:green。
    LINES = [
        LineByTwoPoints(start=startPoint, end=Point2D(90, 46), color=Color(255, 45, 85), name=r"y = (1/2)x + 1"),
        LineByTwoPoints(start=startPoint, end=Point2D(98, 99), color=Color(255, 153, 51), name="y = x + 1"),
        LineByTwoPoints(start=startPoint, end=Point2D(32, 97), color=Color(44, 170, 80), name="y = 3x + 1"),
    ]

    print("=" * 60)
    print(f"起始点 {startPoint}，各直线截距 b = 1")
    print("=" * 60)

    # 白色背景的 RGBA 画布
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # 先画 100×100 栅格（淡灰线）
    draw_grid(draw)

    for line in LINES:
        # 由 start 与 end 反推斜截式 y = kx + b
        k = (line.end.y - line.start.y) / (line.end.x - line.start.x)
        b = line.start.y - k * line.start.x
        x_start, x_end = line.start.x, line.end.x

        # 理想直线（淡色连续，作为栅格化的参考）
        ax0, ay0 = point_to_image(line.start)
        ax1, ay1 = point_to_image(line.end)
        draw.line([(ax0, ay0), (ax1, ay1)],
                  fill=(line.color.red, line.color.green, line.color.blue, int(0.4 * 255)),
                  width=2)

        # 栅格画法：每列只点亮一个最近的栅格单元（仅保留落在 100×100 内的）
        cells = Canvas2D.rasterize_line(k, b, x_start, x_end)
        for c in cells:
            if 0 <= c.y < GRID:
                rect = cell_rect(int(c.x), int(c.y))
                draw.rectangle(rect,
                               fill=(line.color.red, line.color.green, line.color.blue,
                                     int(0.85 * 255)))

    # 坐标轴、刻度标签与标题（复用三角形脚本同一套布局）
    draw_ticks_and_labels(draw, load_font(18), load_font(22), load_font(30),
                          title="直线的朴素栅格画法（按列最邻近）")

    # 保存为 PNG 图片
    OUTPUT_PATH = "graph_line_no_interpolation.png"
    img.save(OUTPUT_PATH)
    print(f"已保存： {OUTPUT_PATH}")

    # 保存后自动打开图片（按平台调用系统默认查看器）
    ImageViewer.open_image(OUTPUT_PATH)


if __name__ == "__main__":
    main()
