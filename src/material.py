from vector import Vector


class Material:
    def __init__(self, ambient, diffuse, specular, alpha):
        self.ambient = Vector(*ambient)
        self.diffuse = Vector(*diffuse)
        self.specular = Vector(*specular)
        self.alpha = alpha
