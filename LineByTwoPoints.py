"""
由“两个端点”定义的直线（两点式，带样式）。

把直线的几何与样式封装成一个独立的数据类，供多个绘制脚本复用，
避免在 main_draw_line_naive.py / main_draw_line_interpolation.py 之间重复定义。

设计说明：
  - 本类用 start / end 两个 Point2D 端点表示“一条直线”，属于“两点式”
    表示法（LineByTwoPoints），与无限长的抽象 Line 区分开。
  - 字段 color / name 是渲染所需的样式信息（颜色与图例名），与纯几何分离。
  - 后续若要以“斜率 + 截距”“一点 + 方向”等其他形式定义直线，可再新增
    相应的表示类（如 LineSlopeIntercept），与本两点式表示互不耦合。
"""

from dataclasses import dataclass

from Color import Color
from Point2D import Point2D


@dataclass(frozen=True)
class LineByTwoPoints:
    """由两点定义的直线（两点式，带样式）。

    start：起点；end：终点；color：RGB 颜色（Color）；name：图例/标签名。
    """

    start: Point2D
    end: Point2D
    color: Color
    name: str
