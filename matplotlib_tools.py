"""配置 Matplotlib 以正确显示中文字符。

把支持中文的字体设置集中封装，避免在多个脚本中重复粘贴配置代码。
在调用任何 Matplotlib 绘图函数之前导入并调用 `configure_chinese_font()` 即可。
"""

import matplotlib
from matplotlib.colors import to_rgba

from Color import Color


def configure_chinese_font():
    """配置支持中文的字体，避免标题/图例中的中文显示为方块。

    macOS 自带 PingFang SC，其余为常见中文回退字体。
    """
    matplotlib.rcParams["font.sans-serif"] = [
        "PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "DejaVu Sans",
    ]
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["axes.unicode_minus"] = False  # 正常显示负号


def color_spec_to_color(color) -> Color:
    """把 matplotlib 颜色规格（如 "red"、(1,0,0)、#ff0000）转成 Color 对象（0~255）。

    供需要把颜色名当作着色基色、再与系数相乘（如 Canvas2D.draw_shaded_triangle
    的 color * h）的场景复用。转换集中在此处，与 Canvas2D「不依赖 matplotlib」
    的边界保持一致——调用方只需拿到纯 Color 对象。
    """
    r, g, b, _ = to_rgba(color)
    return Color(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))
