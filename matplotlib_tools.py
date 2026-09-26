"""配置 Matplotlib 以正确显示中文字符。

把支持中文的字体设置集中封装，避免在多个脚本中重复粘贴配置代码。
在调用任何 Matplotlib 绘图函数之前导入并调用 `configure_chinese_font()` 即可。
"""

import matplotlib


def configure_chinese_font():
    """配置支持中文的字体，避免标题/图例中的中文显示为方块。

    macOS 自带 PingFang SC，其余为常见中文回退字体。
    """
    matplotlib.rcParams["font.sans-serif"] = [
        "PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "DejaVu Sans",
    ]
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["axes.unicode_minus"] = False  # 正常显示负号
