"""
使用 Matplotlib 以栅格画法绘制直线。

设计要点：
  1. 起始点 A = (0, 1)，三条直线均过该点，截距 b = 1。
  2. 用斜截式 y = kx + b 表示直线，斜率 k 与截距 b 直接给定。
  3. x 每次只递增 1 个栅格单位（一个“点”），由 y = kx + b 得到浮点 y，
     再把 y 四舍五入到最近的栅格行——即每次只“点亮”一个栅格单元（最邻近栅格化）。
  4. 使用 Matplotlib 把被点亮的栅格单元（实心方格）画在 100×100 栅格上，
     并用淡色连续直线作为“理想直线”参考，便于对比栅格化误差。
  5. 绘制结果同时保存为 graph_line_no_interpolation.png。
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib_tools import configure_chinese_font
from Point2D import Point2D
from Canvas2D import Canvas2D

# 配置支持中文的字体，避免标题/图例中的中文显示为方块。
configure_chinese_font()


def main():
    GRID = 100
    A = Point2D(0, 1)  # 三条直线的公共起始点 (0,1)

    # 要绘制的多条直线：(终点 P1, 颜色, 图例名)
    # 起点统一为 A=(0,1)，由 A 与 P1 反推斜率 k 与截距 b。
    LINES = [
        (Point2D(90, 46), "tab:red", r"$y = \frac{1}{2}x + 1$"),
        (Point2D(98, 99), "tab:orange", "y = x + 1"),
        (Point2D(32, 97), "tab:green", "y = 3x + 1"),
    ]

    print("=" * 60)
    print(f"起始点 A = {A}，各直线截距 b = 1（均过 (0,1)）")
    print("=" * 60)

    # 用 Matplotlib 绘制
    fig, ax = plt.subplots(figsize=(10, 10))

    # 逐条绘制：淡色“理想直线” + 栅格化点亮的栅格单元
    for p1, color, name in LINES:
        # 由 A 与 p1 反推斜截式 y = kx + b
        k = (p1.y - A.y) / (p1.x - A.x)
        b = A.y - k * A.x
        x_end = p1.x
        # 理想直线（淡色连续，作为栅格化的参考）
        ax.plot([A.x, p1.x], [A.y, p1.y],
                color=color, lw=1.2, alpha=0.4, zorder=2,
                label=f"{name}")

        # 栅格画法：每列只点亮一个最近的栅格单元（仅保留落在 100×100 内的）
        cells = Canvas2D.rasterize_line(k, b, A.x, x_end)
        for x, y in cells:
            if 0 <= y < GRID:
                ax.add_patch(plt.Rectangle((x, y), 1, 1,
                                           facecolor=color, edgecolor="none",
                                           alpha=0.85, zorder=3))
        ax.scatter([], [], s=40, color=color, alpha=0.85,
                   label=f"{name} 栅格")

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
    ax.set_title("直线的无插值式栅格画法")
    ax.legend(loc="upper right")

    plt.tight_layout()
    # 保存为 PNG 图片
    fig.savefig("graph_line_no_interpolation.png", dpi=400)
    print("已保存： graph_line_no_interpolation.png")
    plt.show()


if __name__ == "__main__":
    main()
