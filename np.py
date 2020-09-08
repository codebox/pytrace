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


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def get_intersection_point(rect, line_vector, line_point):
    line_vector = normalize(line_vector)
    n_dot_u = rect.normal @ line_vector # (6)

    w = np.subtract(rect.p1, line_point) # (3)

    s1 = np.where(n_dot_u, -rect.normal.dot(w) / n_dot_u, None) # (6)

    intersection = np.where(s1 is None, np.zeros(3), w + np.transpose(s1 * line_vector) - rect.p1) # (6,3)

    a_m = np.subtract(intersection, rect.p1) # (6,3)
    a_b = np.repeat(np.subtract(rect.p2, rect.p1)[:,np.newaxis], len(a_m), axis=1).T # (6,3)
    a_d = np.repeat(np.subtract(rect.p3, rect.p1)[:,np.newaxis], len(a_m), axis=1).T # (6,3)

    am_dot_ab = np.sum(a_m * a_b, axis=1)   # (6)
    ab_dot_ab = np.sum(a_b * a_b, axis=1)   # (6)
    am_dot_ad = np.sum(a_m * a_d, axis=1)   # (6)
    ad_dot_ad = np.sum(a_d * a_d, axis=1)   # (6)

    c1 = np.logical_and(0 < am_dot_ab, am_dot_ab < ab_dot_ab)
    c2 = np.logical_and(0 < am_dot_ad, am_dot_ad < ad_dot_ad)
    c3 = np.logical_and(c1, c2)

    return np.where(np.repeat(c3[:,np.newaxis], 3, axis=1), intersection, 0)

class Rect:
    def __init__(self, normal, p1, p2, p3):
        self.normal = np.array(normal)
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        self.p3 = np.array(p3)


rect = Rect((0,0,-1), (-1, -1, SCREEN_DISTANCE + 5), (-1, 1, SCREEN_DISTANCE + 5), (1, -1, SCREEN_DISTANCE + 5))

line_vector = np.subtract(pixel_coords, camera_position)
magnitudes = np.linalg.norm(line_vector, axis=1)
unit_line_vector = np.transpose(line_vector) / magnitudes

line_point = camera_position

points = get_intersection_point(rect, unit_line_vector, line_point)
print(points)
img_data = np.zeros_like(points)
for (p, s) in zip(points, line_vector):
    if not (p==[0,0,0]).all():
        img_data




# img = Image.fromarray(points, 'RGB')
# img.save('my.png')
# img.show()