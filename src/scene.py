from vector import Line, Vector, Point
from PIL import Image, ImageDraw
import numpy as np


class Scene:
    def __init__(self, screen, camera_position, background_colour, scale):
        self.screen = screen
        self.camera_position = camera_position
        self.background_colour = background_colour
        self.scale = scale
        self.rectangles = []
        self.lights = []

    def add_object(self, object):
        try:
            [self.rectangles.append(rectangle) for rectangle in object.get_rectangles()]
        except AttributeError:
            self.rectangles.append(object)

    def clear_objects(self):
        self.rectangles = []

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
            for rectangle in self.rectangles:
                if rectangle.get_intersection_point(line_from_point_to_light):
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
        for rectangle in self.rectangles:
            intersection_point_for_current = rectangle.get_intersection_point(camera_to_pixel)
            if intersection_point_for_current:
                intersection_points.append((rectangle, intersection_point_for_current))

        if intersection_points:
            closest_intersection = min(intersection_points, key=lambda p: p[1].distance_to(self.camera_position))
            illumination = self._calculate_illumination(*closest_intersection)
            if illumination:
                return self._blinn_phong_colour(illumination)

        return self.background_colour

    def to_image(self):
        image = Image.new('RGB', (self.screen.width * self.scale, self.screen.height * self.scale), self.background_colour)
        for x in range(self.screen.width * self.scale):
            for y in range(self.screen.height * self.scale):
                colour = self._calculate_pixel_colour(x / self.scale, y / self.scale)
                image.putpixel((x, self.screen.height * self.scale - y - 1), colour)

        return image


class Screen:
    def __init__(self, width, height, distance):
        self.width = width
        self.height = height
        self.distance = distance
