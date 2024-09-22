from pyproj import Transformer


class LambertPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def from_gps(longitude, latitude):
        # Create a transformer to convert from WGS84 (EPSG:4326) to Lambert 1972 (EPSG:31370)
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:31370", always_xy=True)
        x, y = transformer.transform(longitude, latitude)
        return LambertPoint(x, y)
