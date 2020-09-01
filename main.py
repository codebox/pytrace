import math
from PIL import Image, ImageDraw

EPSILON = 0.1

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


class Line:
    def __init__(self, vector, point):
        self.vector = vector
        self.point = point

    def __str__(self):
        return '{} --- {}'.format(self.point, self.vector)

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

    def _calculate_illumination(self, target_object, point):
        if not self.lights:
            return []

        illumination = []
        for light in self.lights:
            shifted_point = target_object.get_camera_side_shifted_point(point, self.camera_position)
            line_from_point_to_light = Line(Vector.from_points(shifted_point, light.position), shifted_point)

            is_illuminated = True
            for object in self.objects:
                if object.get_intersection_point(line_from_point_to_light):
                    is_illuminated = False
                    break

            if is_illuminated:
                illumination.append((
                    target_object,
                    light,
                    line_from_point_to_light.vector.unit(),
                    target_object.plane_normal.unit(),
                    Vector.from_points(shifted_point, self.camera_position).unit()
                ))

        return illumination

    def _blinn_phong_colour(self, illumination_list):
        total_illumination = Vector(0, 0, 0)
        for illumination in illumination_list:
            object, light, point_to_light_vector, surface_normal_vector, point_to_camera_vector = illumination

            ambient = object.ambient.multiply_by_vector(light.ambient)

            l_dot_n = abs(point_to_light_vector.dot_product(surface_normal_vector))
            diffuse = object.diffuse.multiply_by_vector(light.diffuse).multiply(l_dot_n)

            l_v_unit = point_to_light_vector.add_to_vector(point_to_camera_vector).unit()
            specular_factor = abs(surface_normal_vector.dot_product(l_v_unit) ** (object.alpha / 4))
            specular = object.specular.multiply_by_vector(light.specular).multiply(specular_factor)

            total_illumination = total_illumination.add_to_vector(ambient).add_to_vector(diffuse).add_to_vector(specular)

        r, g, b = total_illumination.multiply(255).tuple()

        return int(min(255,r)), int(min(255,g)), int(min(255,b))

    def _calculate_pixel_colour(self, x, y):
        screen_pixel_position = Point(x - self.screen.width / 2, y - self.screen.height / 2, self.screen.distance)
        camera_to_pixel_vector = Vector.from_points(self.camera_position, screen_pixel_position)

        camera_to_pixel = Line(camera_to_pixel_vector, self.camera_position)

        intersection_points = []
        for object in self.objects:
            intersection_point_for_current = object.get_intersection_point(camera_to_pixel)
            if intersection_point_for_current:
                intersection_points.append((object, intersection_point_for_current))

        if intersection_points:
            closest_intersection = min(intersection_points, key=lambda p: p[1].distance_to(self.camera_position))
            illumination = self._calculate_illumination(*closest_intersection)
            if illumination:
                return self._blinn_phong_colour(illumination)

        return self.background_colour

    def render(self, output_file):
        image = Image.new('RGB', (self.screen.width, self.screen.height), self.background_colour)
        for x in range(self.screen.width):
            for y in range(self.screen.height):
                image.putpixel((x, screen.height - y - 1), self._calculate_pixel_colour(x, y))

        image.save(output_file)


class Rectangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ambient = Vector(0.1, 0, 0)
        self.diffuse = Vector(0.7, 0, 0)
        self.specular = Vector(1, 1, 1)
        self.alpha = 100

        p1_p2 = self.p1.vector_to(self.p2)
        p1_p3 = self.p1.vector_to(self.p3)
        self.plane_normal = p1_p2.cross_product(p1_p3)

    def get_intersection_point(self, line):
        line_unit_vector = line.vector.unit()

        n_dot_u = self.plane_normal.dot_product(line_unit_vector)
        if not n_dot_u:
            # The line is parallel to the plane
            return None

        w = Vector.from_points(self.p1, line.point)
        s1 = -self.plane_normal.dot_product(w) / n_dot_u
        if s1 < 0:
            # The intersection point is on the wrong side of line.point
            return None

        intersection = Point(
            w.x + s1 * line_unit_vector.x + self.p1.x,
            w.y + s1 * line_unit_vector.y + self.p1.y,
            w.z + s1 * line_unit_vector.z + self.p1.z
        )
        a_m = Vector.from_points(self.p1, intersection)
        a_b = Vector.from_points(self.p1, self.p2)
        a_d = Vector.from_points(self.p1, self.p3)

        am_dot_ab = a_m.dot_product(a_b)
        ab_dot_ab = a_b.dot_product(a_b)
        am_dot_ad = a_m.dot_product(a_d)
        ad_dot_ad = a_d.dot_product(a_d)

        if (0 < am_dot_ab < ab_dot_ab) and (0 < am_dot_ad < ad_dot_ad):
            return intersection

    def get_camera_side_shifted_point(self, point, camera_position):
        shift_vector = self.plane_normal.unit().multiply(EPSILON)

        p_shifted_1 = point.move(shift_vector)
        p_shifted_2 = point.move(shift_vector.negate())

        p1_camera_distance = p_shifted_1.distance_to(camera_position)
        p2_camera_distance = p_shifted_2.distance_to(camera_position)

        return p_shifted_1 if p1_camera_distance < p2_camera_distance else p_shifted_2


class Light:
    def __init__(self, position):
        self.position = position
        self.ambient = Vector(1, 1, 1)
        self.diffuse = Vector(1, 1, 1)
        self.specular = Vector(1, 1, 1)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_DISTANCE = 1000
screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_DISTANCE)

CAMERA_X = 0
CAMERA_Y = SCREEN_HEIGHT/2
CAMERA_Z = 0
camera_position = Point(CAMERA_X, CAMERA_Y, CAMERA_Z)

COLOUR_BLACK = (0, 0, 0)

scene = Scene(screen, camera_position, COLOUR_BLACK)

floor = Rectangle(
    Point(-SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, SCREEN_DISTANCE),
    Point(-SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, SCREEN_DISTANCE + SCREEN_WIDTH * 20),
    Point( SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, SCREEN_DISTANCE)
)
scene.add_object(floor)

s = 50
cube_center = (0, -SCREEN_HEIGHT/2 + s, SCREEN_DISTANCE + SCREEN_WIDTH)

def point(x,y,z):
    return Point(cube_center[0] + x + 5, cube_center[1] + y + 5, cube_center[2] + z + 5)

top_face = Rectangle(
    point(-s, s, 0),
    point(0, s, -s),
    point(0, s, s)
)
scene.add_object(top_face)

right_face = Rectangle(
    point(0, s, -s),
    point(0, s * (1 - math.sqrt(2)), -s),
    point(s, s, 0)
)
scene.add_object(right_face)

left_face = Rectangle(
    point(0, s, -s),
    point(0,  s * (1 - math.sqrt(2)), -s),
    point(-s, s, 0)
)
scene.add_object(left_face)

light_position = Point(SCREEN_WIDTH/4,SCREEN_HEIGHT,SCREEN_DISTANCE / 2)
light = Light(light_position)
scene.add_light(light)

for i in range(1000):
    light.position.z += 10
    light.position.x -= 1
    scene.render('output{:05}.png'.format(i))