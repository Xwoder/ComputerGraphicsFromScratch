"""
使用 Matplotlib 以栅格画法绘制直线。

设计要点：
  1. 起始点 A = (0, 1)，三条直线均过该点，截距 b = 1。
  2. 用斜截式 y = kx + b 表示直线，斜率 k 与截距 b 直接给定。
  3. x 每次只递增 1 个栅格单位（一个“点”），由 y = kx + b 得到浮点 y，
     再把 y 四舍五入到最近的栅格行——即每次只“点亮”一个栅格单元（最邻近栅格化）。
  4. 使用 Matplotlib 把被点亮的栅格单元（实心方格）画在 100×100 栅格上，
     并用淡色连续直线作为“理想直线”参考，便于对比栅格化误差。
  5. 绘制结果同时保存为 output_line.png。
"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# 配置支持中文的字体，避免标题/图例中的中文显示为方块。
# macOS 自带 PingFang SC，其余为常见中文回退字体。
matplotlib.rcParams["font.sans-serif"] = [
    "PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "DejaVu Sans",
]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False  # 正常显示负号


def rasterize_line(k, intercept, x_start, x_end):
    """栅格画法：x 每次递增 1，由 y = kx + b 得到浮点 y，
    再四舍五入到最近的栅格行，每个 x 只点亮一个栅格单元 (x, round(y))。"""
    cells = []
    x = x_start
    while x <= x_end:
        y = k * x + intercept
        cells.append((x, int(round(y))))  # 最邻近栅格化：每列只点亮一个单元
        x += 1
    return cells


def main():
    GRID = 100
    A = (0, 1)  # 三条直线的公共起始点 (0,1)

    # 要绘制的多条直线：(斜率k, 截距b, 颜色, 绘制终止列x_end, 图例名)
    LINES = [
        (0.5, 1, "tab:red", 90, r"$y = \frac{1}{2}x + 1$"),
        (1.0, 1, "tab:orange", 98, "y = x + 1"),
        (3.0, 1, "tab:green", 32, "y = 3x + 1"),
    ]

    print("=" * 60)
    print(f"起始点 A = {A}，各直线截距 b = 1（均过 (0,1)）")
    for k, b, color, x_end, name in LINES:
        print(f"  {name}： y = {k:.4f} * x + {b:.4f}")
    print("=" * 60)

    # 用 Matplotlib 绘制
    fig, ax = plt.subplots(figsize=(10, 10))

    # 逐条绘制：淡色“理想直线” + 栅格化点亮的栅格单元
    for k, b, color, x_end, name in LINES:
        # 理想直线（淡色连续，作为栅格化的参考）
        ax.plot([0, x_end], [b, k * x_end + b],
                color=color, lw=1.2, alpha=0.4, zorder=2,
                label=f"{name}")

        # 栅格画法：每列只点亮一个最近的栅格单元（仅保留落在 100×100 内的）
        cells = rasterize_line(k, b, A[0], x_end)
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
    fig.savefig("output_line.png", dpi=400)
    print("已保存： output_line.png")
    plt.show()


if __name__ == "__main__":
    main()
