import math
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

    def distance_to(self, other):
        return math.sqrt(
            math.pow(self.x - other.x, 2) +
            math.pow(self.y - other.y, 2) +
            math.pow(self.z - other.z, 2)
        )

class Line:
    def __init__(self, origin, target):
        self.origin = origin
        self.target = target

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

    def _calculate_pixel_colour(self, x, y):
        screen_pixel_position = Point(x - self.screen.width / 2, y - self.screen.height / 2, self.screen.distance)
        camera_to_pixel = Line(self.camera_position, screen_pixel_position)

        intersection_points = []
        for object in self.objects:
            intersection_points_for_current = object.get_intersection_points(camera_to_pixel)
            intersection_points.extend([(object, p) for p in intersection_points_for_current])

        if intersection_points:
            closest_intersection = min(intersection_points, key=lambda p: p[1].distance_to(self.camera_position))
            return closest_intersection[0].colour
        else:
            return self.background_colour

    def render(self, output_file):
        image = Image.new('RGB', (self.screen.width, self.screen.height), self.background_colour)
        for x in range(self.screen.width):
            for y in range(self.screen.height):
                image.putpixel((x,y), self._calculate_pixel_colour(x, y))

        image.save(output_file)


class Sphere:
    def __init__(self, center, radius, colour):
        self.center = center
        self.radius = radius
        self.colour = colour

    def get_intersection_points(self, line):
        return [] #TODO

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
COLOUR_RED = (255, 0, 0)

scene = Scene(screen, camera_position, COLOUR_BLACK)

sphere1 = Sphere(Point(0, 0, 1000), 300, COLOUR_RED)
scene.add_object(sphere1)

scene.add_light(Light())

scene.render('output.png')