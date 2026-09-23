from Color import Color
from Point3 import Point3
from Scene import Scene
from Sphere import Sphere


def createScene() -> Scene:
    """
    创建包含三个球体的场景：红、蓝、绿各一个。

    Returns:
        Scene: 由三个球体构成的场景
    """

    spheres: list[Sphere] = [
        Sphere(center=Point3(0, -1, 3),
               radius=1,
               color=Color(255, 0, 0)),
        Sphere(center=Point3(2, 0, 4),
               radius=1,
               color=Color(0, 0, 255)),
        Sphere(center=Point3(-2, 0, 4),
               radius=1,
               color=Color(0, 255, 0)),
    ]

    return Scene(spheres)


if __name__ == '__main__':
    scene: Scene = createScene()

    for sphere in scene.spheres:
        print(sphere)
