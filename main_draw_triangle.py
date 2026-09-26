"""
使用 Canvas2D.draw_line 以栅格画法绘制三角形线框（wireframe）。

对应 Gabriel Gambetta《Computer Graphics from Scratch》中的
DrawWireframeTriangle(P0, P1, P2, color)：依次用 DrawLine 连接三条边
(P0, P1)、(P1, P2)、(P2, P0)。

实现要点：
  1. 三个顶点 P0/P1/P2 给定后，调用 draw_wireframe_triangle 连出三条边。
  2. 每条边用 Canvas2D.draw_line 做对称插值栅格化，返回被点亮的栅格单元。
  3. 栅格化单元用黑色实心方格绘制在 N×N 栅格上（颜色按题目要求用黑色）；
     另用淡灰连续三角形作为“理想”参考，便于对比栅格化误差。
  4. 绘制结果保存为 graph_triangle.png（使用 Pillow 渲染，不依赖 Matplotlib）。
"""

from typing import cast

from PIL import Image, ImageDraw, ImageFont

from Canvas2D import Canvas2D
from Color import Color
from ImageViewer import ImageViewer
from Point2D import Point2D
from plot_utils import (GRID, SCALE, MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP,
                        MARGIN_BOTTOM, PLOT_W, PLOT_H, W, H, PLOT_LEFT,
                        PLOT_RIGHT, PLOT_TOP, PLOT_BOTTOM, draw_ticks_and_labels)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """加载支持中文的字体；若系统字体不可用则回退到默认字体。

    macOS 自带 STHeiti / Arial Unicode 等中文字体，按顺序尝试。
    """
    candidates = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    # 回退：默认字体不是 FreeTypeFont，按类型转换以满足返回注解
    return cast(ImageFont.FreeTypeFont, ImageFont.load_default())


def cell_rect(cx: int, cy: int) -> list[int]:
    """把栅格单元 (cx, cy) 映射成图像中的像素矩形 [left, top, right, bottom]。

    Pillow 图像原点在左上、y 轴向下，而网格 y 轴向上，故按 (GRID - y) 翻转。
    """
    left = PLOT_LEFT + cx * SCALE
    top = PLOT_BOTTOM - (cy + 1) * SCALE
    right = PLOT_LEFT + (cx + 1) * SCALE
    bottom = PLOT_BOTTOM - cy * SCALE
    return [left, top, right, bottom]


def point_to_image(p: Point2D) -> tuple[float, float]:
    """把网格坐标点映射成图像坐标（用于绘制理想三角形与标签定位）。"""
    return PLOT_LEFT + p.x * SCALE, PLOT_BOTTOM - p.y * SCALE


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    """在绘图区画出 100×100 栅格：次刻度每 1 单元（浅灰）、主刻度每 10 单元（深灰）。"""
    minor = (225, 225, 225, 255)
    major = (160, 160, 160, 255)
    for i in range(GRID + 1):
        x = PLOT_LEFT + i * SCALE
        y = PLOT_TOP + i * SCALE
        # 竖线
        draw.line([(x, PLOT_TOP), (x, PLOT_BOTTOM)],
                  fill=major if i % 10 == 0 else minor, width=1)
        # 横线
        draw.line([(PLOT_LEFT, y), (PLOT_RIGHT, y)],
                  fill=major if i % 10 == 0 else minor, width=1)


def draw_wireframe_triangle(p0: Point2D, p1: Point2D, p2: Point2D):
    """线框三角形：连接 (P0,P1)、(P1,P2)、(P2,P0) 三条边。

    返回三条边被点亮的栅格单元集合（去重），供上层决定绘制颜色。
    对应 Gambetta 的 DrawWireframeTriangle(P0, P1, P2, color)，
    其中 color 仅影响“如何上色”，不影响栅格化结果，故在此不传入。
    """
    cells = set()
    pa: Point2D
    pb: Point2D
    for pa, pb in ((p0, p1), (p1, p2), (p2, p0)):
        line: list[Point2D] = Canvas2D.draw_line(pa, pb)
        cells.update(line)
    return cells


def main() -> None:
    # 颜色与透明度（固定写死，不通过命令行参数配置）
    fill_color = Color.RED
    wire_color = Color.BLACK
    fill_alpha = 0.55

    # 三角形的三个顶点（栅格坐标；整数或浮点均可，draw_line 内部会吸附到最近单元）
    vertices = [Point2D(10, 10), Point2D(90, 40), Point2D(60, 90)]

    # 比较三个点的 Y 轴坐标，按升序排列：
    #   位置最低（Y 最小） -> P0
    #   第二高（Y 居中）   -> P1
    #   最高点（Y 最大）   -> P2
    vertices.sort(key=lambda p: p.y)
    P0, P1, P2 = vertices

    wire_cells = draw_wireframe_triangle(P0, P1, P2)

    # 填充三角形：对每条扫描线取该行的左、右两个端点（左右起点），再用
    # Canvas2D.draw_line 在它们之间画一条水平线段，逐行就把三角形填满——
    # 即“用画线的方法”填充，与线框共用同一个 draw_line 原语。
    scanlines = Canvas2D.fill_triangle_scanlines(P0, P1, P2)
    fill_cells = set()
    for y, xl, xr in scanlines:
        fill_cells.update(Canvas2D.draw_line(Point2D(xl, y), Point2D(xr, y)))

    # ───────────────────── 用 Pillow 渲染 ─────────────────────
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # 1) 栅格
    draw_grid(draw)

    # 2) 把栅格化结果（填充 + 线框）绘制到一张带透明通道的 overlay 上，
    #    再用 alpha_composite 把它合成到主图——这样半透明的填充能透出底下的
    #    栅格线，而黑色的线框保持不透明覆盖在填充之上。
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay, "RGBA")
    for c in fill_cells:
        x, y = int(c.x), int(c.y)
        if 0 <= x < GRID and 0 <= y < GRID:
            col = (fill_color.red, fill_color.green,
                   fill_color.blue, int(255 * fill_alpha))
            ov.rectangle(cell_rect(x, y), fill=col)
    for c in wire_cells:
        x, y = int(c.x), int(c.y)
        if 0 <= x < GRID and 0 <= y < GRID:
            ov.rectangle(cell_rect(x, y),
                         fill=(wire_color.red, wire_color.green,
                               wire_color.blue, 255))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img, "RGBA")

    # 3) 理想三角形（淡灰连续，作为栅格化的参考，置于填充之上便于对比边界）
    outline = (120, 120, 120, 200)
    for a_pt, b_pt in ((P0, P1), (P1, P2), (P2, P0)):
        ax, ay = point_to_image(a_pt)
        bx, by = point_to_image(b_pt)
        draw.line([(ax, ay), (bx, by)], fill=outline, width=3)

    # 4) 三个顶点的文字标签。
    #    P0 是最低点，三角形内部在其上方，故把 P0 标签放到下方（外侧）；
    #    P1/P2 放在上方，既避开黑色栅格单元又不压在三角形内部。
    font_label = load_font(20)
    min_y = min(P0.y, P1.y, P2.y)
    offsets = {"P0": 22, "P1": -22, "P2": -22}
    for label, p in (("P0", P0), ("P1", P1), ("P2", P2)):
        ix, iy = point_to_image(p)
        dy = offsets[label] if p.y > min_y + 1 else 22
        draw.text((ix, iy + dy), label,
                  font=font_label, fill=(0, 0, 0, 255), anchor="mm")

    # 5) 坐标轴、刻度标签与标题
    draw_ticks_and_labels(draw, load_font(18), load_font(22), load_font(30),
                          title="三角形的线框栅格画法")

    OUTPUT_PATH = "graph_triangle.png"
    img.save(OUTPUT_PATH)
    print(f"已保存： {OUTPUT_PATH}，填充 {len(fill_cells)} 个栅格单元，线框 {len(wire_cells)} 个")

    # 保存后自动打开图片（按平台调用系统默认查看器）
    ImageViewer.open_image(OUTPUT_PATH)


if __name__ == "__main__":
    main()
