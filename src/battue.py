from geopy.point import Point
import json


class Poste:
    def __init__(self, poste_json):
        self.number: str = poste_json["number"]  # it's not actually a number, it's a string, but it is usually a number, and sometimes a P or D
        gps_point = poste_json["gps"]
        self.gps_point: Point = Point(gps_point["latitude"], gps_point["longitude"])


class Battue:
    def __init__(self, battue_configuration_file: str):
        file = open(battue_configuration_file, "r")
        json_content = json.load(file)
        file.close()
        self.name: str = json_content["name"]
        self.label: str = json_content["label"]
        self.postes: list(Poste) = []
        for poste_json in json_content["postes"]:
            self.postes.append(Poste(poste_json))
