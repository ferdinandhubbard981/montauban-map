from PIL import ImageFont, ImageDraw, Image
import json
from battue import Battue
from util import LambertPoint


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

    def draw_postes(self, battue: Battue):
        draw = ImageDraw.Draw(self.image)  # created object for image
        # font = ImageFont.truetype("Fontsah.ttf", 40)  # Defined font you can download any font and use it.
        for poste in battue.postes:
            xcor, ycor = self.convert_lambert_to_pixel(poste.lambert_point)
            print(f"{poste.lambert_point.x}, {poste.lambert_point.y}")
            # print(f"{xcor}, {ycor}")
            draw.text((xcor, ycor), poste.number, fill=(0, 0, 0, 255))  # here we draw

    def convert_lambert_to_pixel(self, lambert_point: LambertPoint):
        lambert_diff_y = lambert_point.y - self.top_left_pixel_lambert_point.y
        lambert_diff_x = lambert_point.x - self.top_left_pixel_lambert_point.x
        xcor: int = lambert_diff_x / self.x_pixel_delta
        ycor: int = lambert_diff_y / self.y_pixel_delta
        return xcor, ycor


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
