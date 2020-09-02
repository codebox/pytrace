import math
from vector import Vector, Point
EPSILON = 0.1


class Rectangle:
    def __init__(self, p1, p2, p3, material):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ambient = material.ambient
        self.diffuse = material.diffuse
        self.specular = material.specular
        self.alpha = material.alpha

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

    def __str__(self):
        return '{}--{}--{}'.format(self.p2, self.p1, self.p3)


class Cube:
    def __init__(self, center, side_length, material):
        self.center = center
        self.side_length = side_length
        self.material = material
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0

    def _point(self, x, y, z):
        rotated_x = x * self.side_length / 2
        rotated_y = y * self.side_length / 2
        rotated_z = z * self.side_length / 2

        # apply z-axis rotation
        rotated_x, rotated_y = rotated_x * math.cos(self.z_rotation) - rotated_y * math.sin(self.z_rotation), rotated_x * math.sin(self.z_rotation) + rotated_y * math.cos(self.z_rotation)

        # apply y-axis rotation
        rotated_x, rotated_z = rotated_x * math.cos(self.y_rotation) + rotated_z * math.sin(self.y_rotation), -rotated_x * math.sin(self.y_rotation) + rotated_z * math.cos(self.y_rotation)

        # apply x-axis rotation
        rotated_y, rotated_z = rotated_y * math.cos(self.x_rotation) - rotated_z * math.sin(self.x_rotation), rotated_y * math.sin(self.x_rotation) + rotated_z * math.cos(self.x_rotation)

        return Point(
            rotated_x + self.center.x,
            rotated_y + self.center.y,
            rotated_z + self.center.z
        )

    def _get_top_face(self):
        return Rectangle(
            self._point(-1, 1, -1),
            self._point(-1, 1,  1),
            self._point( 1, 1, -1),
            self.material
        )

    def _get_bottom_face(self):
        return Rectangle(
            self._point(-1, -1, -1),
            self._point(-1, -1,  1),
            self._point( 1, -1, -1),
            self.material
        )

    def _get_front_face(self):
        return Rectangle(
            self._point(-1,  1, -1),
            self._point( 1,  1, -1),
            self._point(-1, -1, -1),
            self.material
        )

    def _get_back_face(self):
        return Rectangle(
            self._point(-1,  1, 1),
            self._point( 1,  1, 1),
            self._point(-1, -1, 1),
            self.material
        )

    def _get_left_face(self):
        return Rectangle(
            self._point(-1,  1, -1),
            self._point(-1,  1,  1),
            self._point(-1, -1, -1),
            self.material
        )

    def _get_right_face(self):
        return Rectangle(
            self._point(1,  1, -1),
            self._point(1,  1,  1),
            self._point(1, -1, -1),
            self.material
        )

    def get_rectangles(self):
        return self._get_back_face(), self._get_front_face(), self._get_left_face(), self._get_right_face(), self._get_top_face(), self._get_bottom_face()

