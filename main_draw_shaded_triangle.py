"""
使用 Canvas2D.draw_shaded_triangle 绘制带插值着色的三角形（Shaded Triangle）。

参考 Gabriel Gambetta《Computer Graphics from Scratch》中的
DrawShadedTriangle(P0, P1, P2, color)：每个顶点带一个 h 着色系数（0~1），
三角形内部每个像素的颜色 = color * h，h 先沿三条边、再沿每条水平扫描线
两次线性插值得到，从而呈现从暗到亮的渐变着色。

坐标参考 main_draw_triangle.py（100×100 栅格），但使用一组新的顶点与 h 值。

绘制结果保存为 graph_shaded_triangle.png（使用 Pillow 渲染，不依赖 Matplotlib）。
"""

from typing import cast

from PIL import Image, ImageDraw, ImageFont

from Canvas2D import Canvas2D
from Color import Color
from ImageViewer import ImageViewer
from Point2D import Point2D

# ───────────────────────── 渲染参数 ─────────────────────────
GRID = 100  # 栅格边长（100×100 单元）
SCALE = 12  # 每个栅格单元对应的像素边长
MARGIN_LEFT = 80  # 左侧留白（放 y 轴刻度标签）
MARGIN_RIGHT = 50
MARGIN_TOP = 90  # 顶部留白（放标题）
MARGIN_BOTTOM = 80  # 底部留白（放 x 轴刻度标签 + 轴名）

# 由 GRID / SCALE / 留白推导出的画布与绘图区尺寸
PLOT_W = GRID * SCALE
PLOT_H = GRID * SCALE
W = MARGIN_LEFT + PLOT_W + MARGIN_RIGHT
H = MARGIN_TOP + PLOT_H + MARGIN_BOTTOM
PLOT_LEFT = MARGIN_LEFT
PLOT_RIGHT = MARGIN_LEFT + PLOT_W
PLOT_TOP = MARGIN_TOP
PLOT_BOTTOM = MARGIN_TOP + PLOT_H  # 栅格 y=0 对应的图像 y（向下为正）


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """加载支持中文的字体；若系统字体不可用则回退到默认字体。

    macOS 自带 STHeiti / Arial Unicode 等中文字体，按顺序尝试。
    """
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc.ttc",
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


def draw_ticks_and_labels(draw: ImageDraw.ImageDraw,
                          font_tick: ImageFont.FreeTypeFont,
                          font_axis: ImageFont.FreeTypeFont,
                          font_title: ImageFont.FreeTypeFont) -> None:
    """绘制坐标轴名（x / y）、主刻度标签（0,10,...,100）与标题。"""
    tick_color = (60, 60, 60, 255)

    # 主刻度标签：每 10 个单位
    for i in range(0, GRID + 1, 10):
        # x 轴刻度标签（位于绘图区下方）
        tx = PLOT_LEFT + i * SCALE
        draw.text((tx, PLOT_BOTTOM + 8), str(i),
                  font=font_tick, fill=tick_color, anchor="ma")
        # y 轴刻度标签（位于绘图区左侧）
        ty = PLOT_BOTTOM - i * SCALE
        draw.text((PLOT_LEFT - 10, ty), str(i),
                  font=font_tick, fill=tick_color, anchor="rm")

    # 轴名
    draw.text((PLOT_RIGHT, PLOT_BOTTOM + 45), "x",
              font=font_axis, fill=(0, 0, 0, 255), anchor="mm")
    draw.text((PLOT_LEFT - 55, PLOT_TOP), "y",
              font=font_axis, fill=(0, 0, 0, 255), anchor="mm")

    # 标题（居中于顶部留白）
    draw.text((W // 2, MARGIN_TOP // 2 + 10),
              "三角形的插值着色（Shaded Triangle）",
              font=font_title, fill=(0, 0, 0, 255), anchor="mm")


def main() -> None:
    # 基色与每个顶点的着色系数 h（固定写死，不通过命令行参数配置）
    base_color = Color.RED
    h0: float = 0.0
    h1: float = 1.0
    h2: float = 0.4
    # 新的三角形顶点（栅格坐标），与线框示例 (10,10)/(90,40)/(60,90) 不同：
    #   顶点顺序与下面的 h 一一对应（draw_shaded_triangle 内部会按 y 排序）。
    P0 = Point2D(15, 20)
    P1 = Point2D(85, 30)
    P2 = Point2D(50, 90)

    canvas = Canvas2D(GRID, GRID)

    # 用 lines 数组描述所有线段：每一项是一个 (start, end) 二元组。
    # 显式保存每条线的起点，这样即便后续各线段起点不再相同（不再是共点扇形），
    # 也无需改动这里的结构。
    lines: list[tuple[Point2D, Point2D]] = [
        (P0, P1),
        (P1, P2),
        (P2, P0),
    ]

    # 先画出三条边的线框（边框像素写入缓冲），随后填充时通过 skip 跳过这些
    # 边框单元，使内部着色不会覆盖原本的边框线（而非事后重绘覆盖）。
    wire_cells: set[tuple[int, int]] = set()
    for start, end in lines:
        for c in Canvas2D.draw_line(start, end):
            wx, wy = int(c.x), int(c.y)
            wire_cells.add((wx, wy))
            canvas.putPixel(wx, wy, (0.0, 0.0, 0.0, 1.0))

    canvas.draw_shaded_triangle(
        P0, P1, P2,
        color=base_color,
        h0=h0, h1=h1, h2=h2,
        skip=wire_cells,
    )

    # ───────────────────── 用 Pillow 渲染 ─────────────────────
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # 1) 栅格
    draw_grid(draw)

    # 2) 把 Canvas2D 帧缓冲逐格绘制（线框 + 着色三角形）
    arr = canvas.as_array()  # shape=(height, width, 4)，行索引 = 栅格 y
    for y in range(GRID):
        for x in range(GRID):
            r, g, b, a = arr[y, x]
            if a <= 0:
                continue
            col = (int(r * 255), int(g * 255), int(b * 255), int(a * 255))
            draw.rectangle(cell_rect(x, y), fill=col)

    # 3) 理想三角形（淡灰连续，作为栅格化的参考，置于着色之上便于对比边界）
    outline = (120, 120, 120, 200)
    for a_pt, b_pt in ((P0, P1), (P1, P2), (P2, P0)):
        ax, ay = point_to_image(a_pt)
        bx, by = point_to_image(b_pt)
        draw.line([(ax, ay), (bx, by)], fill=outline, width=3)

    # 4) 三个顶点的文字标签（含各自的 h 值，便于对照着色渐变）。
    #    最低点（y 最小）的标签放在三角形外侧（下方），其余放在上方，
    #    避免压住着色像素。min_y 提到循环外，避免在 3 次迭代里重复计算。
    font_label = load_font(20)
    min_y = min(P0.y, P1.y, P2.y)
    for label, p, h in (("P0", P0, h0), ("P1", P1, h1), ("P2", P2, h2)):
        ix, iy = point_to_image(p)
        dy = 22 if p.y <= min_y + 1 else -22
        draw.text((ix, iy + dy), f"{label}\nh={h:.1f}",
                  font=font_label, fill=(0, 0, 0, 255), anchor="mm")

    # 5) 坐标轴、刻度标签与标题
    draw_ticks_and_labels(draw, load_font(18), load_font(22), load_font(30))

    OUTPUT_PATH = "graph_shaded_triangle.png"
    img.save(OUTPUT_PATH)
    print(f"已保存： {OUTPUT_PATH}（基色 {base_color}，h0={h0}, h1={h1}, h2={h2}）")

    # 保存后自动打开图片（按平台调用系统默认查看器）
    ImageViewer.open_image(OUTPUT_PATH)


if __name__ == "__main__":
    main()
