"""Pillow 渲染的共享布局参数与坐标轴绘制工具。

多个绘制脚本（main_draw_triangle / main_draw_shaded_triangle 等）都使用同一套
100×100 栅格布局，并把坐标轴、刻度标签与标题的绘制逻辑集中在此，避免重复定义。
"""

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


def draw_ticks_and_labels(draw,
                          font_tick,
                          font_axis,
                          font_title,
                          title: str) -> None:
    """绘制坐标轴名（x / y）、主刻度标签（0,10,...,GRID）与标题 title。

    draw：Pillow 的 ImageDraw 对象；font_tick/axis/title：三个层级的字体；
    title：绘图标题（由调用方按图形含义传入，如“三角形的线框栅格画法”）。
    """
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
              title,
              font=font_title, fill=(0, 0, 0, 255), anchor="mm")
