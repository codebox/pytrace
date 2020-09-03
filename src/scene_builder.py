from material import Material
from light import Light
from objects import Rectangle
from scene import Scene, Screen
from vector import Point

import random

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)


class SceneBuilder:
    def __init__(self, screen, camera_position, scale):
        self.screen = screen
        self.camera_position = camera_position
        self.scale = scale

    def build_flat_plane(self):
        scene = Scene(self.screen, self.camera_position, COLOUR_WHITE, self.scale)

        count = 1
        for x in range(count):
            for y in range(count):
                s = int(self.screen.width / count)
                cube_material = Material(
                    (0 + int(random.random() * 100), 150 + int(random.random() * 100), int(1 * random.random())),
                    # (0,0,255),
                    (0.5, 0.5, 0.5),
                    (0.8, 0.8, 0.8),
                    (0.5, 0.5, 0.5),
                    50
                )
                rectangle = Rectangle(
                    Point(x * s - self.screen.width/2, -self.screen.height / 2, self.screen.distance + y * s),
                    Point(x * s - self.screen.width/2, -self.screen.height / 2, self.screen.distance + (y+1) * s),
                    Point((x+1) * s - self.screen.width/2, -self.screen.height / 2, self.screen.distance + y * s),
                    cube_material
                )
                scene.add_object(rectangle)

        light_position = Point(-self.screen.width/4,-self.screen.height/2 + 50, self.screen.width * 4 + self.screen.distance)
        light = Light(light_position)
        scene.add_light(light)

        return scene
