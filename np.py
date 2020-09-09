import numpy as np
from PIL import Image

w=3
h=3
SCREEN_DISTANCE = 4


x = np.linspace(-w/2, w/2, w)
y = np.linspace(-h/2, h/2, h)

xs = np.tile(x, len(y))
ys = np.repeat(y, len(x))
zs = np.full(len(x) * len(y), SCREEN_DISTANCE)

camera_position = np.array([0,0,0])
pixel_coords = np.transpose([xs, ys, zs])

light_position = np.array([-w/2, h/2, SCREEN_DISTANCE])


class Rect:
    def __init__(self, normal, p1, p2, p3):
        self.normal = np.array(normal)
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        self.p3 = np.array(p3)

    def get_intersection_points(self, ray_origin, ray_directions):
        ray_magnitudes = np.linalg.norm(ray_directions, axis=1)
        rays_normalised = np.transpose(ray_directions) / ray_magnitudes

        n_dot_u = self.normal @ rays_normalised

        w = np.subtract(self.p1, ray_origin)

        s1 = np.where(n_dot_u, -self.normal.dot(w) / n_dot_u, None)

        intersection = np.where(s1 is None, np.zeros(3), w + np.transpose(s1 * rays_normalised) - self.p1)

        a_m = np.subtract(intersection, self.p1)
        a_b = np.repeat(np.subtract(self.p2, self.p1)[:,np.newaxis], len(a_m), axis=1).T
        a_d = np.repeat(np.subtract(self.p3, self.p1)[:,np.newaxis], len(a_m), axis=1).T

        am_dot_ab = np.sum(a_m * a_b, axis=1)
        ab_dot_ab = np.sum(a_b * a_b, axis=1)
        am_dot_ad = np.sum(a_m * a_d, axis=1)
        ad_dot_ad = np.sum(a_d * a_d, axis=1)

        c1 = np.logical_and(0 < am_dot_ab, am_dot_ab < ab_dot_ab)
        c2 = np.logical_and(0 < am_dot_ad, am_dot_ad < ad_dot_ad)
        c3 = np.logical_and(c1, c2)

        return np.where(np.repeat(c3[:,np.newaxis], 3, axis=1), intersection, 0)

rect1 = Rect((0,0,-1), (-1, -1, SCREEN_DISTANCE + 5), (-1, 1, SCREEN_DISTANCE + 5), (1, -1, SCREEN_DISTANCE + 5))
rect2 = Rect((0,0,-1), (-1, -1, SCREEN_DISTANCE + 6), (-1, 1, SCREEN_DISTANCE + 6), (1, -1, SCREEN_DISTANCE + 6))

objects = [rect1, rect2]
rays = np.subtract(pixel_coords, camera_position)

# intersections = [object.get_intersection_points(camera_position, rays) for object in objects]

for object in objects:
    intersections = object.get_intersection_points(camera_position, rays)
    intersections_with_pixels = np.stack((intersections, pixel_coords), axis=1)
    # print(intersections_with_pixels)
    mask = intersections_with_pixels[:,0].any(axis=1)
    print(mask)
    hits = np.compress(mask, intersections_with_pixels, axis=0)
    print(hits)
    # print(np.extract(intersections_with_pixels[0] == 0, intersections_with_pixels))
    # print(np.extract(np.compress(np.all(intersections_with_pixels[0] == 0), intersections_with_pixels, axis=0)))
    # actual = np.extract(intersections != [0,0,0], intersections)
    #
    # intersections_to_light = np.subtract(intersections, light_position)
    # print(intersections_to_light)


# img = Image.fromarray(points, 'RGB')
# img.save('my.png')
# img.show()