"""
使用 Canvas2D.draw_shaded_triangle 绘制带插值着色的三角形（Shaded Triangle）。

参考 Gabriel Gambetta《Computer Graphics from Scratch》中的
DrawShadedTriangle(P0, P1, P2, color)：每个顶点带一个 h 着色系数（0~1），
三角形内部每个像素的颜色 = color * h，h 先沿三条边、再沿每条水平扫描线
两次线性插值得到，从而呈现从暗到亮的渐变着色。

坐标参考 main_draw_triangle.py（100×100 栅格），但使用一组新的顶点与 h 值。

绘制结果保存为 graph_shaded_triangle.png。
"""

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.ticker import MultipleLocator

from matplotlib_tools import configure_chinese_font
from Point2D import Point2D
from Canvas2D import Canvas2D
from Color import Color

# 配置支持中文的字体，避免标题/图例中的中文显示为方块。
configure_chinese_font()


def main(base_color: str = "red",
         h0: float = 0.0,
         h1: float = 1.0,
         h2: float = 0.4) -> None:
    GRID = 100
    # 新的三角形顶点（栅格坐标），与线框示例 (10,10)/(90,40)/(60,90) 不同：
    #   顶点顺序与下面的 h 一一对应（draw_shaded_triangle 内部会按 y 排序）。
    P0 = Point2D(15, 20)
    P1 = Point2D(85, 30)
    P2 = Point2D(50, 90)

    # 把颜色名（如 "red"）转成 0~255 的 Color 对象，供着色缩放使用
    r, g, b, _ = to_rgba(base_color)
    base_color_obj = Color(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))

    canvas = Canvas2D(GRID, GRID)
    canvas.draw_shaded_triangle(
        P0, P1, P2,
        color=base_color_obj,
        h0=h0, h1=h1, h2=h2,
    )

    # 用 Matplotlib 绘制
    fig, ax = plt.subplots(figsize=(10, 10))

    # 坐标轴与栅格（与第一、三象限正半轴对齐）：先定范围
    ax.set_xlim(0, GRID)
    ax.set_ylim(0, GRID)
    ax.set_aspect("equal", adjustable="box")
    # 主刻度每 10 个单位（带坐标标签）
    ax.set_xticks(range(0, GRID + 1, 10))
    ax.set_yticks(range(0, GRID + 1, 10))
    # 次刻度每 1 个单位 -> 画出真正的 100×100 栅格
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.grid(True, which="major", color="gray", lw=0.8)
    ax.grid(True, which="minor", color="lightgray", lw=0.25)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("三角形的插值着色（Shaded Triangle）")

    # 理想三角形（淡灰连续，作为栅格化的参考，置于着色之上便于对比边界）
    ax.plot([P0.x, P1.x, P2.x, P0.x],
            [P0.y, P1.y, P2.y, P0.y],
            color="gray", lw=1.2, alpha=0.6, zorder=3)

    # 把 Canvas2D 帧缓冲交给 imshow 渲染（每个单元 1×1，放大不留缝）
    ax.imshow(canvas.as_array(), origin="lower", extent=(0, GRID, 0, GRID),
              interpolation="nearest", zorder=2)

    # 三个顶点的文字标签（含各自的 h 值，便于对照着色渐变）。
    # 最低点（y 最小）的标签放在三角形外侧（下方），其余放在上方，
    # 避免压住着色像素。min_y 提到循环外，避免在 3 次迭代里重复计算。
    min_y = min(P0.y, P1.y, P2.y)
    for label, p, h in (("P0", P0, h0), ("P1", P1, h1), ("P2", P2, h2)):
        dy = -3 if p.y <= min_y + 1 else 1
        ax.text(p.x, p.y + dy, f"{label}\nh={h:.1f}",
                fontsize=12, color="black", ha="center", zorder=4)

    plt.tight_layout()
    OUTPUT_PATH = "graph_shaded_triangle.png"
    fig.savefig(OUTPUT_PATH, dpi=400)
    print(f"已保存： {OUTPUT_PATH}（基色 {base_color}，h0={h0}, h1={h1}, h2={h2}）")
    plt.show()


if __name__ == "__main__":
    import sys
    # 可选：python main_draw_shaded_triangle.py [base_color] [h0] [h1] [h2]
    # 例：python main_draw_shaded_triangle.py red 0 1 0.4
    args = sys.argv[1:]
    color = args[0] if len(args) >= 1 else "red"
    try:
        hv = [float(a) for a in args[1:4]]
    except ValueError:
        hv = []
    h0 = hv[0] if len(hv) >= 1 else 0.0
    h1 = hv[1] if len(hv) >= 2 else 1.0
    h2 = hv[2] if len(hv) >= 3 else 0.4
    main(base_color=color, h0=h0, h1=h1, h2=h2)
