"""
用 Rasterizer.renderInstances 渲染两个立方体线框网格（模型实例化）。

对应 Gabriel Gambetta《Computer Graphics from Scratch》中把网格顶点投影后
用画线法绘制三角面的栅格化管线：
- 立方体由 geometry.Model.create_cube() 构建一次（8 个 Point3 顶点 + 12 个
  Triangle，每个三角面自带 color：红/绿/蓝/黄/紫/青分面着色）；
- 用 geometry.Instance 把同一模型摆放到两个不同位置（transform.translation），实现物体复用；
- Rasterizer 内部调用 Camera.projectVertex 把每个实例顶点透视投影到画布像素，
  再逐三角面用 DrawWireframeTriangle 画三条边（线框）；
- 结果写入 3D Canvas，最终保存为 PPM。

该脚本不依赖 numpy，仅复用项目已有的 Camera / Canvas / Viewport /
Model / Instance / Rasterizer，可独立运行。
"""

import sys
from pathlib import Path

# 把项目根目录加入 sys.path（仅当尚未存在时），保证顶层导入始终可用。
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fractions import Fraction

from Camera import Camera
from Canvas import Canvas
from Number import Number
from Instance import Instance
from model.Model import Model
from geometry.Point3 import Point3
from geometry.Vec3 import Vec3
from Rasterizer import Rasterizer
from Rotation import Rotation
from Transform import Transform
from Viewport import Viewport


if __name__ == '__main__':
    ASPECT_RATIO: Fraction = Fraction(1, 1)

    CANVAS_WIDTH: int = 800
    CANVAS_HEIGHT: int = int(CANVAS_WIDTH / ASPECT_RATIO)
    canvas: Canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # 视口宽高比与画布保持一致（4:3），距离 d = 1（projectVertex 内部用作透视除法分母）。
    viewportWidth: Number = 1
    viewportHeight: Number = float(viewportWidth / ASPECT_RATIO)
    viewport: Viewport = Viewport(width=viewportWidth,
                                  height=viewportHeight,
                                  distance=1.0)

    camera = Camera()  # 原点 (0,0,0)，看向 +z
    rasterizer = Rasterizer(canvas, camera, viewport)

    # 用 Model.create_cube() 构建一个共享的立方体模型。严格按 RenderInstance 伪代码，
    # 实例只靠 transform 摆放（缩放=1、无旋转），故把世界位置并入 transform.translation
    # （相机在原点看向 +z，故 z 需为正）。两个实例复用同一个 cube 模型（物体复用 / 实例化）：
    #   - 实例 1：translation = (-1.5, 0, 7)
    #   - 实例 2：translation = (1.25, 2, 7.5)
    cube = Model.create_cube()
    instances = [
        Instance(cube,
                 position=Point3(0, 0, 0),
                 transform=Transform(1, Rotation(0, 0, 0), Vec3(-1.5, 0, 7))),
        Instance(cube,
                 position=Point3(0, 0, 0),
                 transform=Transform(1, Rotation(0, 0, 0), Vec3(1.25, 2, 7.5))),
    ]

    # 渲染所有实例：每个 Instance 的顶点先经 transform（缩放→旋转→平移）变换，
    # 再透视投影，最后逐三角面用模型自带 color 画三条边（线框，backFaceCulling=False）。
    rasterizer.renderInstances(instances)

    # 输出到项目根目录下的 output/（相对本脚本位置解析，运行目录无关）。
    OUTPUT_PATH: Path = Path(__file__).resolve().parent.parent / "output" / "main_draw_two_cubes.ppm"
    canvas.savePPM(OUTPUT_PATH)
    print(f"saved: {OUTPUT_PATH}")
