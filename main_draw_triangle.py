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
  4. 绘制结果保存为 graph_triangle.png。
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib_tools import configure_chinese_font
from Point2D import Point2D
from Canvas2D import Canvas2D

# 配置支持中文的字体，避免标题/图例中的中文显示为方块。
configure_chinese_font()


def draw_wireframe_triangle(p0: Point2D, p1: Point2D, p2: Point2D):
    """线框三角形：连接 (P0,P1)、(P1,P2)、(P2,P0) 三条边。

    返回三条边被点亮的栅格单元集合（去重），供上层决定绘制颜色。
    对应 Gambetta 的 DrawWireframeTriangle(P0, P1, P2, color)，
    其中 color 仅影响“如何上色”，不影响栅格化结果，故在此不传入。
    """
    cells = set()
    for a, b in ((p0, p1), (p1, p2), (p2, p0)):
        cells.update(Canvas2D.draw_line(a, b))
    return cells


def main():
    GRID = 100
    # 三角形的三个顶点（栅格坐标；整数或浮点均可，draw_line 内部会吸附到最近单元）
    vertices = [Point2D(10, 10), Point2D(90, 40), Point2D(60, 90)]

    # 比较三个点的 Y 轴坐标，按升序排列：
    #   位置最低（Y 最小） -> P0
    #   第二高（Y 居中）   -> P1
    #   最高点（Y 最大）   -> P2
    vertices.sort(key=lambda p: p.y)
    P0, P1, P2 = vertices

    wire_cells = draw_wireframe_triangle(P0, P1, P2)
    fill_cells = Canvas2D.draw_filled_triangle(P0, P1, P2)

    # 用 Matplotlib 绘制
    fig, ax = plt.subplots(figsize=(10, 10))

    # 理想三角形（淡灰连续，作为栅格化的参考，本身不是三角形线框的颜色）
    ax.plot([P0.x, P1.x, P2.x, P0.x],
            [P0.y, P1.y, P2.y, P0.y],
            color="gray", lw=1.2, alpha=0.4, zorder=1)

    # 填充三角形：红色实心方格（按题目要求使用红色），置于底层
    for x, y in fill_cells:
        if 0 <= x < GRID and 0 <= y < GRID:
            ax.add_patch(plt.Rectangle((x, y), 1, 1,
                                       facecolor="red", edgecolor="none",
                                       alpha=0.55, zorder=2))

    # 线框三角形：黑色实心方格描边，置于填充之上，凸显边界
    for x, y in wire_cells:
        if 0 <= x < GRID and 0 <= y < GRID:
            ax.add_patch(plt.Rectangle((x, y), 1, 1,
                                       facecolor="black", edgecolor="none",
                                       alpha=0.9, zorder=3))

    # 三个顶点的文字标签。
    # P0 是最低点，三角形内部在其上方，故把 P0 标签放到下方（外侧）；
    # P1/P2 放在右上方，既避开黑色栅格单元又不压在三角形内部。
    offsets = {"P0": (0, -2), "P1": (0, -2), "P2": (0, 1)}
    for label, p in (("P0", P0), ("P1", P1), ("P2", P2)):
        dx, dy = offsets[label]
        ax.text(p.x + dx, p.y + dy, label,
                fontsize=14, color="black", zorder=4)

    # 坐标轴与栅格（与第一、三象限正半轴对齐）
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
    ax.set_title("三角形的线框栅格画法（Wireframe Triangle）")

    plt.tight_layout()
    # 保存为 PNG 图片
    OUTPUT_PATH = "graph_triangle.png"
    fig.savefig(OUTPUT_PATH, dpi=400)
    print(f"已保存： {OUTPUT_PATH}，填充 {len(fill_cells)} 个栅格单元，线框 {len(wire_cells)} 个")
    plt.show()


if __name__ == "__main__":
    main()
