"""Pillow 渲染的共享布局参数与坐标轴绘制工具。

多个绘制脚本（main_draw_triangle / main_draw_shaded_triangle 等）都使用同一套
100×100 栅格布局，并把坐标轴、刻度标签与标题的绘制逻辑集中在此，避免重复定义。
"""

from typing import cast

from PIL import ImageDraw, ImageFont


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


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    """在绘图区画出 GRID×GRID 栅格：次刻度每 1 单元（浅灰）、主刻度每 10 单元（深灰）。"""
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


def cell_rect(cx: int, cy: int) -> list[int]:
    """把栅格单元 (cx, cy) 映射成图像中的像素矩形 [left, top, right, bottom]。

    Pillow 图像原点在左上、y 轴向下，而网格 y 轴向上，故按 (GRID - y) 翻转。
    """
    left = PLOT_LEFT + cx * SCALE
    top = PLOT_BOTTOM - (cy + 1) * SCALE
    right = PLOT_LEFT + (cx + 1) * SCALE
    bottom = PLOT_BOTTOM - cy * SCALE
    return [left, top, right, bottom]


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


# macOS 自带中文字体候选（按顺序尝试）。注意 STHeiti Medium 正确扩展名为 .ttc，
# 旧代码里曾误写成 ".ttc.ttc" 导致该候选失效；此处已修正并合并两脚本的候选。
_FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """加载支持中文的字体；若系统字体不可用则回退到默认字体。

    macOS 自带 STHeiti / Arial Unicode 等中文字体，按顺序尝试。
    """
    for path in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    # 回退：默认字体不是 FreeTypeFont，按类型转换以满足返回注解
    return cast(ImageFont.FreeTypeFont, ImageFont.load_default())
