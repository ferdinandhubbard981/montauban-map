import csv
from util import LambertPoint, postes_csv_path
import numpy as np


class Poste:
    def __init__(self, poste_csv, battue_name):
        self.battue_name = battue_name
        self.number: str = poste_csv["name"]  # it's not actually a number, it's a string, but it is usually a number, and sometimes a P or D
        self.lambert_point: LambertPoint = LambertPoint.from_gps(poste_csv["longitude"], poste_csv["latitude"])
        x_number_offset = poste_csv["number_offset_x"]
        y_number_offset = poste_csv["number_offset_y"]

        if x_number_offset != '' and y_number_offset != '':
            self.number_offset = np.array([int(x_number_offset), int(y_number_offset)])
        else:
            self.number_offset = np.array([0, 0])

        x_line_offset = poste_csv["line_offset_x"]
        y_line_offset = poste_csv["line_offset_y"]
        if x_line_offset != '' and y_line_offset != '':
            self.line_offset = np.array([int(x_line_offset), int(y_line_offset)])
        else:
            self.line_offset = np.array([0, 0])

    def get_point_as_tuple(self):
        return (self.lambert_point.x, self.lambert_point.y)


class Battue:
    def __init__(self, battue_json: str):
        self.name: str = battue_json["name"]
        self.label: str = battue_json["label"]
        self.postes: list(Poste) = []
        self.parity = battue_json["parity"]
        self.colour = battue_json["colour"]
        postes_csv_file = open(postes_csv_path, newline='')
        postes_csv_reader = csv.DictReader(postes_csv_file, delimiter=';')
        for row in postes_csv_reader:
            if row["battue"] == self.name:
                self.postes.append(Poste(row, self.name))
        postes_csv_file.close()
