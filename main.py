from PIL import Image, ImageDraw

class Scene:
    def __init__(self, screen, background_colour = (0,0,0)):
        self.screen_width, self.screen_height = screen
        self.background_colour = background_colour
        self.objects = []
        self.lights = []

    def add_object(self, object):
        self.objects.append(object)

    def add_light(self, light):
        self.lights.append(light)

    def render(self, output_file):
        image = Image.new('RGB', (self.screen_width, self.screen_height), self.background_colour)
        image.save(output_file)


class Sphere:
    pass

class Light:
    pass

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200

scene = Scene((SCREEN_WIDTH, SCREEN_HEIGHT))
scene.add_object(Sphere())
scene.add_light(Light())
scene.render('output.png')