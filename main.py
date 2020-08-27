class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.lights = []

    def add_object(self, object):
        self.objects.append(object)

    def add_light(self, light):
        self.lights.append(light)

    def render(self, output_file):
        pass

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