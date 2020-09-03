from renderer import ImageRenderer
from scene import Screen
from scene_builder import SceneBuilder
from vector import Point

if __name__ == '__main__':
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 200
    SCREEN_DISTANCE = 400
    screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_DISTANCE)

    CAMERA_X = 0
    CAMERA_Y = SCREEN_HEIGHT
    CAMERA_Z = 0
    camera_position = Point(CAMERA_X, CAMERA_Y, CAMERA_Z)

    SCALE = 1

    scene = SceneBuilder(screen, camera_position, SCALE).build_flat_plane()

    ImageRenderer(scene).render('trace.png')
