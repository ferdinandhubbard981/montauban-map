from PIL import ImageFont, ImageDraw, Image
import aggdraw
import json
from battue import Battue
from util import LambertPoint, get_lines_from_vertices, Line, point_within_bounds, flatten_tuple_array
import numpy as np
from shapely import centroid, Polygon

poste_distance_from_line = 10


class ImageCoordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map:
    def __init__(self, image_file_path: str, image_configuration_filename: str):
        pixel_lambert_point_1, pixel_lambert_point_2 = parse_image_data(image_configuration_filename)
        self.image = Image.open(image_file_path)
        self.x_pixel_delta = (pixel_lambert_point_2[1].x - pixel_lambert_point_1[1].x) / (pixel_lambert_point_2[0].x - pixel_lambert_point_1[0].x)  # longitude changes when moving in the x direction
        self.y_pixel_delta = (pixel_lambert_point_2[1].y - pixel_lambert_point_1[1].y) / (pixel_lambert_point_2[0].y - pixel_lambert_point_1[0].y)   # latitude changes when moving in the y direction
        self.top_left_pixel_lambert_point = LambertPoint(pixel_lambert_point_1[1].x - pixel_lambert_point_1[0].x * self.x_pixel_delta, pixel_lambert_point_1[1].y - pixel_lambert_point_1[0].y * self.y_pixel_delta)

    def draw_battue_name(self, battue: Battue):
        draw = ImageDraw.Draw(self.image)  # created object for image
        anchor_point = centroid(Polygon(self.get_line_vertices(battue)))
        draw.text((anchor_point.x, anchor_point.y), battue.name, anchor="mm", fill=(0, 0, 0, 255))
        # draw.textbbox((anchor_point.x, anchor_point.y), battue.name, anchor="mm", stroke_width=20, font_size=20)

    def draw_postes(self, battue: Battue):
        draw = ImageDraw.Draw(self.image)  # created object for image
        # font = ImageFont.truetype("Fontsah.ttf", 40)  # Defined font you can download any font and use it.
        line_vertices = self.get_line_vertices(battue)
        for poste in battue.postes:
            xcor, ycor = self.convert_lambert_to_pixel(poste.lambert_point)
            point = self.adjust_poste_point((xcor, ycor), battue.parity, line_vertices)
            # point = np.array([xcor, ycor])
            draw.text((point[0], point[1]), poste.number, anchor="mm", fill=(0, 0, 0, 255))

    def draw_line(self, battue: Battue):
        draw = aggdraw.Draw(self.image)  # created object for image
        draw.setantialias(True)
        pen = aggdraw.Pen("red", 3.0)
        poste_pixel_coordinate_list = self.get_line_vertices(battue, dup_first=True)
        poste_pixel_coordinate_list = flatten_tuple_array(poste_pixel_coordinate_list)
        draw.line(poste_pixel_coordinate_list, pen)
        draw.flush()
        # draw.polygon(poste_pixel_coordinate_list, width=4, outline="red")

    def convert_lambert_to_pixel(self, lambert_point: LambertPoint):
        lambert_diff_y = lambert_point.y - self.top_left_pixel_lambert_point.y
        lambert_diff_x = lambert_point.x - self.top_left_pixel_lambert_point.x
        xcor: int = lambert_diff_x / self.x_pixel_delta
        ycor: int = lambert_diff_y / self.y_pixel_delta
        return xcor, ycor

    def get_line_vertices(self, battue: Battue, dup_first=False):
        poste_pixel_coordinate_list: [(int, int)] = []
        for poste in battue.postes:
            poste_pixel_coordinate = (self.convert_lambert_to_pixel(poste.lambert_point))
            poste_pixel_coordinate_list.append(poste_pixel_coordinate)
        if dup_first:
            poste_pixel_coordinate_list.append(poste_pixel_coordinate_list[0])
        return poste_pixel_coordinate_list

    def draw_circle(self, point):
        draw = ImageDraw.Draw(self.image)  # created object for image
        draw.circle(point, 5, fill="green")

    def draw_vecline(self, line: Line, color: str):
        linelen = 1000
        draw = ImageDraw.Draw(self.image)  # created object for image
        start = line.get_point_along_line(-linelen / 2)
        end = line.get_point_along_line(linelen / 2)
        draw.line(np.array([start, end]).flatten().tolist(), width=2, fill=color)

    def adjust_poste_point(self, poste_point: (int, int), poste_parity: int, line_vertices: [(int, int)]):  # adjust such that it is not too close to any of the edges of the battue, this takes care of corner postes

        poste_point = np.array(poste_point)
        lines = get_lines_from_vertices(line_vertices)
        for line in lines:
            npline = Line.from_tuple_points(line[0], line[1])
            npline.normalise()
            perpendicular_line = npline.get_perpendicular(poste_point)
            perpendicular_line.normalise()
            # get perpendicular line that passes through poste_point
            intersection_point = Line.get_intersection_point(npline, perpendicular_line)
            if not point_within_bounds(line, intersection_point):
                continue
            distance = np.sqrt(np.sum(np.square(intersection_point - poste_point)))
            if distance < poste_distance_from_line:
                # self.draw_vecline(npline, "blue")
                # self.draw_vecline(perpendicular_line, "green")
                # self.draw_circle(intersection_point)
                perpendicular_line = Line(perpendicular_line.d_vector, intersection_point)
                poste_point = perpendicular_line.get_point_along_line(poste_distance_from_line * poste_parity)

        return poste_point


def parse_image_data(image_configuration_filename: str):
    # with open(image_configuration_filename, "r") as image_configuration_file:
    image_configuration_file = open(image_configuration_filename, "r")
    image_conf = json.load(image_configuration_file)
    image_configuration_file.close()
    point1_json = image_conf["map"]["points"][0]
    pixel_lambert_point_1: (ImageCoordinate, LambertPoint) = (ImageCoordinate(point1_json["image_coordinate"]["x"], point1_json["image_coordinate"]["y"]), LambertPoint.from_gps(point1_json["gps"]["longitude"], point1_json["gps"]["latitude"]))
    point2_json = image_conf["map"]["points"][1]
    pixel_lambert_point_2: (ImageCoordinate, LambertPoint) = (ImageCoordinate(point2_json["image_coordinate"]["x"], point2_json["image_coordinate"]["y"]), LambertPoint.from_gps(point2_json["gps"]["longitude"], point2_json["gps"]["latitude"]))
    return pixel_lambert_point_1, pixel_lambert_point_2
