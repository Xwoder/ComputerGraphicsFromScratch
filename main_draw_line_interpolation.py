"""
使用 Pillow 以插值（Interpolate + DrawLine 算法）栅格画法绘制直线。

设计要点：
  1. 本版本对应 main_draw_line_naive.py 的“无插值”画法，但采用 Gabriel Gambetta
     《Computer Graphics from Scratch》中的对称直线算法：
     - Interpolate(i0, d0, i1, d1)：沿主坐标轴每步进 1，线性插值出另一个坐标。
     - DrawLine(P0, P1)：比较 |Δx| 与 |Δy| 决定“主轴”：
         · |Δx| > |Δy|（偏水平）：x 为主轴，向上插值 y；
         · 否则（偏竖直）：y 为主轴，向上插值 x。
       这样无论平缓还是陡峭的直线，都沿主轴每步只点亮一个栅格单元，
       避免了“无插值”版本在陡峭直线（每列只取最近行）下出现的失真。
  2. 三条直线都过公共起始点 A = (0, 1)：
         - y = 0.5x + 1
         - y = x + 1
         - y = 3x + 1   （陡峭，最能体现插值版本与无插值版本的差异）
  3. 用 Pillow 把被点亮的栅格单元（实心方格）画在 100×100 栅格上，
     并用淡色连续直线作为“理想直线”参考，便于对比栅格化误差。
  4. 绘制结果保存为 graph_line_with_interpolation.png。
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
    # 起点统一为 A=(0,1)（均过 (0,1)），颜色用 Color（RGB 0~255）表示，
    # 对应原 matplotlib 的 tab:red / tab:orange / tab:green。
    LINES = [
        LineByTwoPoints(start=startPoint, end=Point2D(90, 46), color=Color(255, 45, 85), name=r"y = (1/2)x + 1"),
        LineByTwoPoints(start=startPoint, end=Point2D(98, 99), color=Color(255, 153, 51), name="y = x + 1"),
        LineByTwoPoints(start=startPoint, end=Point2D(32, 97), color=Color(44, 170, 80), name="y = 3x + 1"),
    ]

    print("=" * 60)
    print(f"起始点 {startPoint}，各直线截距 b = 1，使用插值法栅格化")
    print("=" * 60)

    # 白色背景的 RGBA 画布
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # 先画 100×100 栅格（淡灰线）
    draw_grid(draw)

    for line in LINES:
        # 理想直线（淡色连续，作为栅格化的参考）
        ax0, ay0 = point_to_image(line.start)
        ax1, ay1 = point_to_image(line.end)
        draw.line([(ax0, ay0), (ax1, ay1)],
                  fill=(line.color.red, line.color.green, line.color.blue, int(0.4 * 255)),
                  width=2)

        # 插值栅格化：沿主轴每步点亮一个最近的栅格单元（仅保留落在 100×100 内）
        cells = Canvas2D.draw_line(line.start, line.end)
        print(f"  {line.name}：点亮 {len(cells)} 个栅格单元")
        for c in cells:
            if 0 <= c.x < GRID and 0 <= c.y < GRID:
                rect = cell_rect(int(c.x), int(c.y))
                draw.rectangle(rect,
                               fill=(line.color.red, line.color.green, line.color.blue,
                                     int(0.85 * 255)))

    # 坐标轴、刻度标签与标题（复用三角形脚本同一套布局）
    draw_ticks_and_labels(draw, load_font(18), load_font(22), load_font(30),
                          title="直线的插值栅格画法（DrawLine）")

    # 保存为 PNG 图片
    OUTPUT_PATH = "graph_line_with_interpolation.png"
    img.save(OUTPUT_PATH)
    print(f"已保存： {OUTPUT_PATH}")

    # 保存后自动打开图片（按平台调用系统默认查看器）
    ImageViewer.open_image(OUTPUT_PATH)


if __name__ == "__main__":
    main()
