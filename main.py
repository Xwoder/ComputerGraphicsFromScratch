from pathlib import Path

from Light.AmbientLight import AmbientLight
from Camera import Camera
from Canvas import Canvas
from Color import Color
from Light.DirectionalLight import DirectionalLight
from Light.Light import Light
from Number import Number
from Point3 import Point3
from Light.PointLight import PointLight
from Renderer import Renderer
from Scene import Scene
from Sphere import Sphere
from Vec3 import Vec3
from Viewport import Viewport

if __name__ == '__main__':
    from fractions import Fraction

    ASPECT_RATIO: Fraction = Fraction(4, 3)

    CANVAS_WIDTH: int = 800
    CANVAS_HEIGHT: int = int(CANVAS_WIDTH / ASPECT_RATIO)
    canvas: Canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    # 视口宽高比与画布保持一致（800:600 = 4:3），避免图像被拉伸。
    # 视口宽度取 1（世界单位）：过宽会让视野(FOV)过大，导致球体显得过小而完整落在画面内；
    # 取 1 时三个球会因超出画面边界而被裁切，符合预期。
    viewportWidth: Number = 1
    viewportHeight: Number = float(viewportWidth / ASPECT_RATIO)
    viewport: Viewport = Viewport(width=viewportWidth,
                                  height=viewportHeight,
                                  distance=1.0)
    camera: Camera = Camera()

    spheres: list[Sphere] = [
        Sphere(center=Point3(0, -1, 3), radius=1, color=Color(255, 0, 0), specular=500, reflective=0.2),
        Sphere(center=Point3(-2, 0, 4), radius=1, color=Color(0, 0, 255), specular=500, reflective=0.3),
        Sphere(center=Point3(2, 0, 4), radius=1, color=Color(0, 255, 0), specular=10, reflective=0.4),
        Sphere(center=Point3(0, -5001, 0), radius=5000, color=Color(255, 255, 0), specular=1000, reflective=0.5),
    ]
    lights: list[Light] = [
        AmbientLight(0.2),
        PointLight(0.6, Point3(2, 1, 0)),
        DirectionalLight(0.6, Vec3(1, 4, 4)),
    ]
    scene: Scene = Scene(spheres=spheres, lights=lights)

    renderer: Renderer = Renderer(scene, canvas, camera, viewport)
    renderer.render()

    OUTPUT_PATH: Path = Path("output.ppm")
    canvas.savePPM(OUTPUT_PATH)
    print(f"saved: {OUTPUT_PATH}")
