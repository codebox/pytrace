from vector import Vector


class Light:
    def __init__(self, position):
        self.position = position
        self.ambient = Vector(1, 1, 1)
        self.diffuse = Vector(1, 1, 1)
        self.specular = Vector(1, 1, 1)
