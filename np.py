import numpy as np
from PIL import Image

w=30
h=30
x_range=3
y_range=3
SCREEN_DISTANCE = 4


x = np.linspace(-x_range/2, x_range/2, w)
y = np.linspace(-y_range/2, y_range/2, h)

xs = np.tile(x, len(y))
ys = np.repeat(y, len(x))
zs = np.full(len(x) * len(y), SCREEN_DISTANCE)

camera_position = np.array([0,0,0])
pixel_coords = np.transpose([xs, ys, zs])

light_position = np.array([-w/2, h/2, SCREEN_DISTANCE])

class Material:
    def __init__(self, rgb, ambient, diffuse, specular, alpha):
        self.rgb = np.array(rgb)
        self.ambient = self.rgb * np.array(ambient)
        self.diffuse = self.rgb * np.array(diffuse)
        self.specular = self.rgb * np.array(specular)
        self.alpha = alpha

class Rect:
    def __init__(self, p1, p2, p3, material):
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        self.p3 = np.array(p3)

        normal = np.cross(self.p2-self.p1, self.p3-self.p1)
        self.normal = normal / np.linalg.norm(normal)
        self.material = material

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

        return np.where(np.repeat(c3[:,np.newaxis], 3, axis=1), intersection, np.nan)

red_material   = Material((255,0,0), (0.5, 0.5, 0.5), (0.8, 0.8, 0.8), (0.5, 0.5, 0.5), 50)
rect1 = Rect((-1, -1, SCREEN_DISTANCE + 7), (-1, 10, SCREEN_DISTANCE + 7), (10, -1, SCREEN_DISTANCE + 7), red_material)

green_material = Material((0,255,0), (0.5, 0.5, 0.5), (0.8, 0.8, 0.8), (0.5, 0.5, 0.5), 50)
rect2 = Rect((-1, -1, SCREEN_DISTANCE + 6),  (-1, 1, SCREEN_DISTANCE + 6),  (1, -1, SCREEN_DISTANCE + 6), green_material)

objects = [rect1, rect2]
rays = np.subtract(pixel_coords, camera_position)

intersections = np.array([object.get_intersection_points(camera_position, rays) for object in objects]).astype(np.float64)

distances = np.linalg.norm(intersections, axis=2)

FAR_AWAY=np.inf
object_indexes_with_smallest_distances = np.argmin(np.nan_to_num(distances, nan=FAR_AWAY), axis=0)

mask_for_all_nan_pixels = np.isnan(distances).all(axis=0)

object_indexes_with_smallest_distances_and_hits = np.where(~mask_for_all_nan_pixels, object_indexes_with_smallest_distances, np.nan)

pixel_colour_indexes = np.copy(object_indexes_with_smallest_distances_and_hits)
pixel_colour_indexes[np.isnan(pixel_colour_indexes)] = len(objects)


background_rgb = (0,0,0)
colours = np.full((h * w,3), background_rgb)
for i in range(len(objects)):
    colours = np.where(np.transpose(np.array([pixel_colour_indexes==i] * 3)), np.full((h*w,3), objects[i].material.rgb), colours)
print(colours)

# colour_choices = np.array([np.full((h*w,3), object.rgb) for object in objects] + [background_pixels])
# print(np.transpose(pixel_colour_indexes.astype(np.int)).shape, colour_choices[0].shape)
# # print(pixel_colour_indexes.shape, colour_choices.shape)
#
# colours = np.array((*pixel_colour_indexes.shape,3))
# print(colour_choices.ravel())
# colours = np.take_along_axis(colour_choices.ravel(), pixel_colour_indexes.astype(np.int), axis=0)


# pixel_colours_for_hits = np.choose(pixel_colour_indexes, ...)

# colour_choices = np.array()
# background_rgb = (0,0,0)
# pixels = np.full((h * w, 3), background_rgb)
# for i in range(len(objects)):
#     colour = objects[i].rgb
#     pixels = np.choose()

# colours = np.choose(object_indexes_with_smallest_distances)
# indexes_of_closest_intersections =

# intersections = np.array([np.reshape(object.get_intersection_points(camera_position, rays), (h,w,3)) for object in objects])
# print(intersections)
#
# intersections_as_grid = np.reshape(intersections, (h,w,3))

# background_colour = np.full((h, w, 3), (0,0,0))
#
# object_colour = np.full((h, w, 3), (255,0,0))
#
# '''
# [[nan nan nan]
#  [nan nan nan]
#  [nan nan nan]
#  [nan nan nan]
#  [0.0 0.0 -9.0]
#  [nan nan nan]
#  [nan nan nan]
#  [nan nan nan]
#  [nan nan nan]]
# '''
# intersections = object.get_intersection_points(camera_position, rays)
#
#
# '''
# [[[nan nan nan] [nan nan nan]  [nan nan nan]]
#  [[nan nan nan] [0.0 0.0 -9.0] [nan nan nan]]
#  [[nan nan nan] [nan nan nan]  [nan nan nan]]]
# '''
# intersections_with_pixels_as_grid = np.reshape(intersections, (h,w,3))
#
# colours = np.where(np.isnan(intersections_with_pixels_as_grid.astype(np.float64)), background_colour, object_colour)
# # distances = hits
# # print(intersections_with_pixels)
# # print(hits)
#
#

colours = np.reshape(colours, (h,w,3))
img = Image.fromarray(colours.astype(np.uint8), 'RGB')
img.save('my.png')
img.show()