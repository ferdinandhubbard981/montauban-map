from pyproj import Transformer
import numpy as np

class LambertPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def from_gps(longitude, latitude):
        # Create a transformer to convert from WGS84 (EPSG:4326) to Lambert 1972 (EPSG:31370)
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:31370", always_xy=True)
        x, y = transformer.transform(longitude, latitude)
        return LambertPoint(x, y)


def get_lines_from_vertices(vertices: [(int, int)]):
    lines: [((int, int), (int, int))] = []
    for i in range(len(vertices) - 1):
        line = (vertices[i], vertices[i + 1])
        lines.append(line)
    lines.append((vertices[len(vertices) - 1], vertices[0]))  # add line between last and first
    return lines


class Line:
    def __init__(self, d_vector: np.array, p_vector: np.array):
        self.d_vector = d_vector
        self.p_vector = p_vector

    def from_tuple_points(point1: (float, float), point2: (float, float)):
        point1 = [point1[0], point1[1]]
        point2 = [point2[0], point2[1]]
        p_vector = np.array(point1)
        point1 = np.array(point1)
        point2 = np.array(point2)
        d_vector = point2 - point1
        return Line(d_vector, p_vector)

    def get_point_along_line(self, t):
        return self.p_vector + self.d_vector * t

    def get_perpendicular(self, p_vector: np.array):
        d_vector = (self.d_vector[1], -self.d_vector[0])
        return Line(d_vector, p_vector)

    def get_intersection_point(line1, line2):
        d1 = line1.d_vector
        d2 = line2.d_vector
        p1 = line1.p_vector
        p2 = line2.p_vector

        u = ((p2[1] - p1[1]) * d1[0] - (p2[0] - p1[0]) * d1[1]) / (d2[0] * d1[1] - d2[1] * d1[0])

        out = line2.get_point_along_line(u)
        return out

    def normalise(self):
        scale = np.sqrt(np.sum(np.square(self.d_vector)))
        d_vector = self.d_vector / scale
        self.d_vector = d_vector


def point_within_bounds(bounds: ((float, float), (float, float)), intersection_point: (float, float)):
    x_values = np.array([bounds[0][0], bounds[1][0]])
    y_values = np.array([bounds[0][1], bounds[1][1]])
    x_values = np.sort(x_values)
    y_values = np.sort(y_values)
    if intersection_point[0] < x_values[0] or intersection_point[0] > x_values[1] or intersection_point[1] < y_values[0] or intersection_point[1] > y_values[1]:
        return False
    return True


def flatten_tuple_array(tuple_array):
    out = []
    for i in tuple_array:
        out.append(i[0])
        out.append(i[1])
    return out


def draw_text_in_a_box(draw, text, colour, anchor_point, fnt, y_offset, padding):
    anchor_point = anchor_point + np.array([0, y_offset])
    left, top, right, bottom = draw.textbbox((anchor_point[0], anchor_point[1]), text, font=fnt, anchor="mm", align="center")
    text_box = [(left - padding, top - padding), (right + padding, bottom + padding)]
    draw.rectangle(text_box, fill="white", outline="black", width=2)
    draw.text((anchor_point[0], anchor_point[1]), text, font=fnt, fill=colour, anchor="mm", align="center")


def pixel_distance(point1, point2):
    temp = point1 - point2
    distance = np.sqrt(np.dot(temp.T, temp))
    return distance


def parse_optional_int_to_str(string_int: str):
    if string_int == '':
        return 0
    else:
        out = int(string_int)
        print(f"out: {out}")
        return out

