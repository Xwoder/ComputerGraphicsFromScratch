"""
使用插值（Interpolate + DrawLine 算法）以栅格画法绘制直线。

设计要点：
  1. 本版本对应 main_draw_line.py 的“无插值”画法，但采用 Gabriel Gambetta
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
  3. 用 Matplotlib 把被点亮的栅格单元（实心方格）画在 100×100 栅格上，
     并用淡色连续直线作为“理想直线”参考，便于对比栅格化误差。
  4. 绘制结果保存为 graph_line_with_interpolation.png。
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
    A = Point2D(0, 1)  # 三条直线的公共起始点

    # 要绘制的多条直线：(终点 P1, 颜色, 图例名)
    # 起点统一为 A=(0,1)，终点按各直线方程 y = kx + b 计算。
    LINES = [
        (Point2D(90, 46), "tab:red", r"$y = \frac{1}{2}x + 1$"),   # k=0.5, 终点 x=90
        (Point2D(98, 99), "tab:orange", "y = x + 1"),              # k=1.0, 终点 x=98
        (Point2D(32, 97), "tab:green", "y = 3x + 1"),              # k=3.0, 陡峭，终点 x=32
    ]

    print("=" * 60)
    print(f"起始点 A = {A}，各直线截距 b = 1（均过 (0,1)），使用插值法栅格化")
    print("=" * 60)

    # 用 Matplotlib 绘制
    fig, ax = plt.subplots(figsize=(10, 10))

    for p1, color, name in LINES:
        # 理想直线（淡色连续，作为栅格化的参考）
        ax.plot([A.x, p1.x], [A.y, p1.y],
                color=color, lw=1.2, alpha=0.4, zorder=2,
                label=f"{name}")

        # 插值栅格化：沿主轴每步点亮一个最近的栅格单元（仅保留落在 100×100 内）
        cells = Canvas2D.draw_line(A, p1)
        print(f"  {name}：点亮 {len(cells)} 个栅格单元")
        for x, y in cells:
            if 0 <= x < GRID and 0 <= y < GRID:
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
    ax.set_title("直线的插值式栅格画法")
    ax.legend(loc="upper right")

    plt.tight_layout()
    # 保存为 PNG 图片
    OUTPUT_PATH = "graph_line_with_interpolation.png"
    fig.savefig(OUTPUT_PATH, dpi=400)
    print(f"已保存： {OUTPUT_PATH}")
    plt.show()


if __name__ == "__main__":
    main()
