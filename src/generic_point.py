import csv
import os
from util import LambertPoint


class GenericPoint:
    def __init__(self, row):
        self.name: str = row["name"]
        self.lambert_point: LambertPoint = LambertPoint.from_gps(
            float(row["longitude"]), float(row["latitude"])
        )
        colour = row.get("colour") if row.get("colour") else None
        self.colour: str = colour.strip() if colour else "red"


def load_generic_points(csv_path: str):
    """Load generic points from a CSV file. Returns an empty list if the file is missing."""
    if not csv_path or not os.path.isfile(csv_path):
        return []
    points = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row.get("name") or not row.get("latitude") or not row.get("longitude"):
                continue
            points.append(GenericPoint(row))
    return points
