from geopy.point import Point
import csv


class Poste:
    def __init__(self, poste_csv):
        self.number: str = poste_csv["name"]  # it's not actually a number, it's a string, but it is usually a number, and sometimes a P or D
        self.gps_point: Point = Point(poste_csv["latitude"], poste_csv["longitude"])


class Battue:
    def __init__(self, battue_json: str):
        self.name: str = battue_json["name"]
        self.label: str = battue_json["label"]
        self.postes: list(Poste) = []
        postes_csv_file = open("../content/postes.csv", newline='')
        postes_csv_reader = csv.DictReader(postes_csv_file, delimiter=';')
        for row in postes_csv_reader:
            if row["battue"] == self.name:
                self.postes.append(Poste(row))
        postes_csv_file.close()
