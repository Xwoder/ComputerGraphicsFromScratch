from pathlib import Path

from Camera import Camera
from Canvas import Canvas
from Color import Color
from Number import Number
from Point3 import Point3
from Renderer import Renderer
from Scene import Scene
from Sphere import Sphere
from Viewport import Viewport

if __name__ == '__main__':
    CANVAS_WIDTH: int = 800
    CANVAS_HEIGHT: int = 600
    canvas: Canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    # 视口宽高比与画布保持一致（800:600 = 4:3），避免图像被拉伸。
    # 视口宽度取 1（世界单位）：过宽会让视野(FOV)过大，导致球体显得过小而完整落在画面内；
    # 取 1 时三个球会因超出画面边界而被裁切，符合预期。
    viewportWidth: Number = 1
    viewport: Viewport = Viewport(width=viewportWidth,
                                  height=viewportWidth * CANVAS_HEIGHT / CANVAS_WIDTH,
                                  distance=1.0)
    camera: Camera = Camera()

    spheres: list[Sphere] = [
        Sphere(center=Point3(0, -1, 3), radius=1, color=Color(255, 0, 0)),
        Sphere(center=Point3(2, 0, 4), radius=1, color=Color(0, 0, 255)),
        Sphere(center=Point3(-2, 0, 4), radius=1, color=Color(0, 255, 0)),
    ]
    scene: Scene = Scene(spheres)

    renderer: Renderer = Renderer(scene, canvas, camera, viewport)
    renderer.render()

    OUTPUT_PATH: Path = Path("output.ppm")
    canvas.savePPM(OUTPUT_PATH)
    print(f"saved: {OUTPUT_PATH}")
