import math
from objects import Rectangle, Cube
from material import Material
from light import Light
from scene import Scene, Screen
from vector import Point
from renderer import ImageRenderer, VideoRenderer


if __name__ == '__main__':
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 200
    SCALE = 1
    SCREEN_DISTANCE = 1000
    screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_DISTANCE)

    CAMERA_X = 0
    CAMERA_Y = SCREEN_HEIGHT
    CAMERA_Z = 0
    camera_position = Point(CAMERA_X, CAMERA_Y, CAMERA_Z)

    COLOUR_BLACK = (0, 0, 0)

    scene = Scene(screen, camera_position, COLOUR_BLACK, SCALE)

    floor_material = Material(
        (255, 255, 255),
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        100
    )
    cube1_material = Material(
        (255,100,50),
        (0.5, 0.5, 0.5),
        (1, 1, 1),
        (0.5, 0.5, 0.5),
        100
    )

    cube = Cube(Point(0, 0, SCREEN_DISTANCE + SCREEN_WIDTH), 50, cube1_material)

    floor = Rectangle(
        Point(-SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, SCREEN_DISTANCE),
        Point(-SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, SCREEN_DISTANCE + SCREEN_WIDTH * 2),
        Point( SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, SCREEN_DISTANCE),
        floor_material
    )

    light_position = Point(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_DISTANCE / 2)
    light = Light(light_position)
    scene.add_light(light)

    scene.add_object(cube)
    scene.add_object(floor)

    ImageRenderer(scene).render('trace.png')
