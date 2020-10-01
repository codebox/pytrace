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

class Light:
    def __init__(self, position, rgb, ambient, diffuse, specular):
        self.position = np.array(position)
        self.rgb = np.array(rgb)
        self.ambient = self.rgb * np.array(ambient)
        self.diffuse = self.rgb * np.array(diffuse)
        self.specular = self.rgb * np.array(specular)

light = Light((-w/2, h/2, SCREEN_DISTANCE), (255,255,255), (1,1,1), (1,1,1), (1,1,1))

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
        self.normal = normal / np.linalg.norm(normal, axis=1).reshape(-1,1)
        self.material = material

    def get_intersection_points(self, ray_origin, ray_directions):
        ray_magnitudes = np.linalg.norm(ray_directions, axis=1)
        rays_normalised = np.transpose(ray_directions) / ray_magnitudes

        n_dot_u = self.normal @ rays_normalised

        w = np.subtract(self.p1, ray_origin)

        x1 = np.einsum('ij,ij->i', self.normal, w)
        x = -x1[:,None] / n_dot_u
        s1 = np.where(n_dot_u, x, None)

        x3 = np.transpose(s1[:,None] * rays_normalised, (2,0,1))
        x2 = w + x3 - self.p1
        intersection = np.where(s1 is None, np.zeros(3), x2)

        a_m = np.transpose(np.subtract(intersection, self.p1), (1,0,2))
        a_b = np.transpose(np.repeat(np.subtract(self.p2, self.p1)[:,np.newaxis], len(a_m[1]), axis=1).T, (2,1,0))
        a_d = np.transpose(np.repeat(np.subtract(self.p3, self.p1)[:,np.newaxis], len(a_m[1]), axis=1).T, (2,1,0))

        am_dot_ab = np.sum(a_m * a_b, axis=2)
        ab_dot_ab = np.sum(a_b * a_b, axis=2)
        am_dot_ad = np.sum(a_m * a_d, axis=2)
        ad_dot_ad = np.sum(a_d * a_d, axis=2)

        c1 = np.logical_and(0 < am_dot_ab, am_dot_ab < ab_dot_ab)
        c2 = np.logical_and(0 < am_dot_ad, am_dot_ad < ad_dot_ad)
        c3 = np.logical_and(c1, c2)

        r = np.transpose(np.repeat(c3[:,np.newaxis], 3, axis=1),(0,2,1))
        i = np.transpose(intersection, (1,0,2))
        return np.where(r, i, np.nan)

    def __len__(self):
        return len(self.p1)

red_material   = Material((255,0,0), (0.5, 0.5, 0.5), (0.8, 0.8, 0.8), (0.5, 0.5, 0.5), 50)
green_material = Material((0,255,0), (0.5, 0.5, 0.5), (0.8, 0.8, 0.8), (0.5, 0.5, 0.5), 50)

objects = Rect(
    ((-1, -1, SCREEN_DISTANCE + 7), (-1, -1, SCREEN_DISTANCE + 6)),
    ((-1, 10, SCREEN_DISTANCE + 7), (-1,  1, SCREEN_DISTANCE + 6)),
    ((10, -1, SCREEN_DISTANCE + 7), ( 1, -1, SCREEN_DISTANCE + 6)),
    (red_material, green_material)
)


rays = np.subtract(pixel_coords, camera_position)

intersections = objects.get_intersection_points(camera_position, rays).astype(np.float64)

distances = np.linalg.norm(intersections, axis=2)

FAR_AWAY=np.inf
object_indexes_with_smallest_distances = np.argmin(np.nan_to_num(distances, nan=FAR_AWAY), axis=0)

mask_for_all_nan_pixels = np.isnan(distances).all(axis=0)

object_indexes_with_smallest_distances_and_hits = np.where(~mask_for_all_nan_pixels, object_indexes_with_smallest_distances, np.nan)

pixel_colour_indexes = np.copy(object_indexes_with_smallest_distances_and_hits)
pixel_colour_indexes[np.isnan(pixel_colour_indexes)] = len(objects)


background_rgb = (0,0,0)
material_colours = np.vstack([[m.rgb for m in objects.material], background_rgb])
colours = material_colours[pixel_colour_indexes.astype(int)]
print(colours)


colours = np.reshape(colours, (h,w,3))
img = Image.fromarray(colours.astype(np.uint8), 'RGB')
img.save('my.png')
img.show()