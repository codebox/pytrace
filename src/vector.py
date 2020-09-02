import math


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def from_points(p1, p2):
        return Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

    def unit(self):
        magnitude = self.magnitude()
        return Vector(
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude,
            )

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        return math.sqrt(
            math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2)
        )

    def negate(self):
        return Vector(-self.x, -self.y, -self.z)

    def multiply(self, factor):
        return self.multiply_by_vector(Vector(factor, factor, factor))

    def multiply_by_vector(self, other):
        return Vector(self.x * other.x, self.y * other.y, self.z * other.z)

    def add_to_vector(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def tuple(self):
        return self.x, self.y, self.z

    def __str__(self):
        return '<{},{},{}>'.format(self.x, self.y, self.z)


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def vector_to(self, other):
        return Vector(
            other.x - self.x,
            other.y - self.y,
            other.z - self.z
        )

    def distance_to(self, other):
        return self.vector_to(other).magnitude()

    def move(self, movement_vector):
        return Point(
            self.x + movement_vector.x,
            self.y + movement_vector.y,
            self.z + movement_vector.z
        )

    def __str__(self):
        return '({},{},{})'.format(self.x, self.y, self.z)


class Line:
    def __init__(self, vector, point):
        self.vector = vector
        self.point = point

    def __str__(self):
        return '{} --- {}'.format(self.point, self.vector)
