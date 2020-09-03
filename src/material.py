from vector import Vector


class Material:
    def __init__(self, rgb, ambient, diffuse, specular, alpha):
        self.ambient = self._vector(rgb, ambient)
        self.diffuse = self._vector(rgb, diffuse)
        self.specular = self._vector(rgb, specular)
        self.alpha = alpha

    def _vector(self, rgb, values):
        r, g, b = rgb
        rv, gv, bv = values
        return Vector(r * rv / 255, g * gv / 255, b * bv / 255)
