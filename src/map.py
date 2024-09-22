from PIL import ImageFont, ImageDraw, Image
from geopy.point import Point
import json
from battue import Battue


class ImageCoordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map:
    def __init__(self, image_file_path: str, image_configuration_filename: str):
        pixel_gps_point_1, pixel_gps_point_2 = parse_image_data(image_configuration_filename)
        self.image = Image.open(image_file_path)
        self.longitude_pixel_delta = (pixel_gps_point_2[1].longitude - pixel_gps_point_1[1].longitude) / (pixel_gps_point_2[0].x - pixel_gps_point_1[0].x)  # longitude changes when moving in the x direction
        self.latitude_pixel_delta = (pixel_gps_point_2[1].latitude - pixel_gps_point_1[1].latitude) / (pixel_gps_point_2[0].y - pixel_gps_point_1[0].y)   # latitude changes when moving in the y direction
        self.top_left_pixel_gps_val = Point(pixel_gps_point_1[1].latitude - pixel_gps_point_1[0].y * self.latitude_pixel_delta, pixel_gps_point_1[1].longitude - pixel_gps_point_1[0].x * self.longitude_pixel_delta)

    def draw_postes(self, battue: Battue):
        draw = ImageDraw.Draw(self.image)  # created object for image
        # font = ImageFont.truetype("Fontsah.ttf", 40)  # Defined font you can download any font and use it.
        for poste in battue.postes:
            xcor, ycor = self.convert_gps_to_pixel(poste.gps_point)
            draw.text((xcor, ycor), poste.number, fill=(0, 0, 0, 255))  # here we draw

    def convert_gps_to_pixel(self, gps_point: Point):
        gps_diff_latitude = gps_point.latitude - self.top_left_pixel_gps_val.latitude
        gps_diff_longitude = gps_point.longitude - self.top_left_pixel_gps_val.longitude
        xcor: int = gps_diff_longitude / self.longitude_pixel_delta
        ycor: int = gps_diff_latitude / self.latitude_pixel_delta
        return xcor, ycor


def parse_image_data(image_configuration_filename: str):
    # with open(image_configuration_filename, "r") as image_configuration_file:
    image_configuration_file = open(image_configuration_filename, "r")
    image_conf = json.load(image_configuration_file)
    image_configuration_file.close()
    point1_json = image_conf["map"]["points"][0]
    pixel_gps_point_1: (ImageCoordinate, Point) = (ImageCoordinate(point1_json["image_coordinate"]["x"], point1_json["image_coordinate"]["y"]), Point(point1_json["gps"]["latitude"], point1_json["gps"]["longitude"]))
    point2_json = image_conf["map"]["points"][1]
    pixel_gps_point_2: (ImageCoordinate, Point) = (ImageCoordinate(point2_json["image_coordinate"]["x"], point2_json["image_coordinate"]["y"]), Point(point2_json["gps"]["latitude"], point2_json["gps"]["longitude"]))
    return pixel_gps_point_1, pixel_gps_point_2
