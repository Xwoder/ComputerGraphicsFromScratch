"""
用透视投影绘制一个线框立方体（wireframe cube）。

对应 Gabriel Gambetta《Computer Graphics from Scratch》的 DrawWireframeCube：
- 立方体的 8 个顶点以相机空间（camera space）下的 Vec3 给出；
- 用 Camera.projectVertex 把每个顶点透视投影到画布像素坐标；
- 用 Canvas.draw_line（Bresenham 整数直线栅格化）连出 12 条棱边：
  前面 4 条为蓝色，后面 4 条为红色，连接前后的 4 条为绿色。

该脚本不依赖 Canvas2D / numpy，仅复用项目已有的 Camera / Canvas / Viewport /
Color / Vec3，可独立运行。

为了让脚本“独立”——无论从哪个工作目录、用何种方式（python / uv run）调用，
都能找到项目根下的 Camera / geometry 等模块——这里先把项目根目录加入 sys.path。
（项目根即本脚本的上一级目录；geometry 内部已统一用 `from geometry.X import X`，
故只需项目根在路径上即可。）
"""

import sys
from pathlib import Path

from geometry.Point2 import Point2

# 把项目根目录加入 sys.path（仅当尚未存在时），保证下面的顶层导入始终可用。
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fractions import Fraction

from Camera import Camera
from Canvas import Canvas
from color.Color import Color
from Number import Number
from geometry.Point3 import Point3
from Viewport import Viewport
from ImageViewer import ImageViewer

if __name__ == '__main__':
    ASPECT_RATIO: Fraction = Fraction(4, 3)

    CANVAS_WIDTH: int = 800
    CANVAS_HEIGHT: int = int(CANVAS_WIDTH / ASPECT_RATIO)
    canvas: Canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # 视口宽高比与画布保持一致（4:3），距离 d = 1（projectVertex 内部用作透视除法分母）。
    viewportWidth: Number = 1
    viewportHeight: Number = float(viewportWidth / ASPECT_RATIO)
    viewport: Viewport = Viewport(width=viewportWidth,
                                  height=viewportHeight,
                                  distance=1.0)


    # 便捷封装：相机空间顶点（Point3 位置点）→ 画布像素坐标（Point2）。
    def project(point3: Point3) -> Point2:
        vertex: Point2 = Camera.projectVertex(canvas, viewport, point3)
        return vertex


    # 立方体的 8 个顶点（相机空间下的空间位置点，单位与视口一致）。
    # 前面（front）z = 5，后面（back）z = 6。
    vAf: Point3 = Point3(-2, -0.5, 5)
    vBf: Point3 = Point3(-2, 0.5, 5)
    vCf: Point3 = Point3(-1, 0.5, 5)
    vDf: Point3 = Point3(-1, -0.5, 5)

    vAb: Point3 = Point3(-2, -0.5, 6)
    vBb: Point3 = Point3(-2, 0.5, 6)
    vCb: Point3 = Point3(-1, 0.5, 6)
    vDb: Point3 = Point3(-1, -0.5, 6)

    # 前面（蓝色）
    canvas.drawLine(project(vAf), project(vBf), Color.BLUE)
    canvas.drawLine(project(vBf), project(vCf), Color.BLUE)
    canvas.drawLine(project(vCf), project(vDf), Color.BLUE)
    canvas.drawLine(project(vDf), project(vAf), Color.BLUE)

    # 后面（红色）
    canvas.drawLine(project(vAb), project(vBb), Color.RED)
    canvas.drawLine(project(vBb), project(vCb), Color.RED)
    canvas.drawLine(project(vCb), project(vDb), Color.RED)
    canvas.drawLine(project(vDb), project(vAb), Color.RED)

    # 前后连接棱（绿色）
    canvas.drawLine(project(vAf), project(vAb), Color.GREEN)
    canvas.drawLine(project(vBf), project(vBb), Color.GREEN)
    canvas.drawLine(project(vCf), project(vCb), Color.GREEN)
    canvas.drawLine(project(vDf), project(vDb), Color.GREEN)

    # 输出到项目根目录下的 output/（相对本脚本位置解析，运行目录无关）。
    OUTPUT_PATH: Path = Path(__file__).resolve().parent.parent / "output" / "graph_cube.ppm"
    canvas.savePPM(OUTPUT_PATH)
    print(f"saved: {OUTPUT_PATH}")

    # 渲染完成后用系统默认查看器打开图片（复用项目已有的 ImageViewer）。
    ImageViewer.openImage(str(OUTPUT_PATH))
