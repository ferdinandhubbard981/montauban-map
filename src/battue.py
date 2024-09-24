import csv
from util import LambertPoint


class Poste:
    def __init__(self, poste_csv):
        self.number: str = poste_csv["name"]  # it's not actually a number, it's a string, but it is usually a number, and sometimes a P or D
        self.lambert_point: LambertPoint = LambertPoint.from_gps(poste_csv["longitude"], poste_csv["latitude"])

    def get_point_as_tuple(self):
        return (self.lambert_point.x, self.lambert_point.y)


class Battue:
    def __init__(self, battue_json: str):
        self.name: str = battue_json["name"]
        self.label: str = battue_json["label"]
        self.postes: list(Poste) = []
        self.parity = battue_json["parity"]
        postes_csv_file = open("../content/postes.csv", newline='')
        postes_csv_reader = csv.DictReader(postes_csv_file, delimiter=';')
        for row in postes_csv_reader:
            if row["battue"] == self.name:
                self.postes.append(Poste(row))
        postes_csv_file.close()
