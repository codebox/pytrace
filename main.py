from PIL import Image, ImageDraw

class Screen:
    def __init__(self, width, height, distance):
        self.width = width
        self.height = height
        self.distance = distance

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Scene:
    def __init__(self, screen, camera_position, background_colour):
        self.screen = screen
        self.camera_position = camera_position
        self.background_colour = background_colour
        self.objects = []
        self.lights = []

    def add_object(self, object):
        self.objects.append(object)

    def add_light(self, light):
        self.lights.append(light)

    def render(self, output_file):
        image = Image.new('RGB', (self.screen.width, self.screen.height), self.background_colour)
        image.save(output_file)


class Sphere:
    pass

class Light:
    pass

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200
SCREEN_DISTANCE = 1000
screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_DISTANCE)

CAMERA_X = 0
CAMERA_Y = 0
CAMERA_Z = 0
camera_position = Point(CAMERA_X, CAMERA_Y, CAMERA_Z)

COLOUR_BLACK = (0, 0, 0)

scene = Scene(screen, camera_position, COLOUR_BLACK)
scene.add_object(Sphere())
scene.add_light(Light())
scene.render('output.png')