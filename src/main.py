from PIL import Image
from geopy.point import Point


class ImageCoordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map:
    def __init__(self, image_file_path: str, pixel_gps_point_1: (ImageCoordinate, Point), pixel_gps_point_2: (ImageCoordinate, Point)):
        self.image = Image.open(image_file_path)
        self.longitude_pixel_delta = (pixel_gps_point_2[1].longitude - pixel_gps_point_1[1].longitude) / (pixel_gps_point_2[0].x - pixel_gps_point_1[0].x)  # longitude changes when moving in the x direction
        self.latitude_pixel_delta = (pixel_gps_point_2[1].latitude - pixel_gps_point_1[1].latitude) / (pixel_gps_point_2[0].y - pixel_gps_point_1[0].y)   # latitude changes when moving in the y direction
        self.top_left_pixel_gps_val = Point(pixel_gps_point_1[1].latitude - pixel_gps_point_1[0].y * self.latitude_pixel_delta, pixel_gps_point_1[1].longitude - pixel_gps_point_1[0].x * self.longitude_pixel_delta)


def main():
    map = Map("../content/saint-leger.jpg", (ImageCoordinate(1, 5), Point(41.5, 81)), (ImageCoordinate(5, 9), Point(45.5, 88)))
    print(map.latitude_pixel_delta)


if __name__ == "__main__":
    main()
