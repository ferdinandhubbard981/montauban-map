from map import Map
from battue import Battue


def main():
    map = Map("../content/saint-leger.png", "../content/saint-leger.json")
    print(f"longitude_pixel_delta: {map.longitude_pixel_delta}")
    forgettes = Battue("../content/battues/forgettes.json")
    print(f"forgettes postes len: {len(forgettes.postes)}")


if __name__ == "__main__":
    main()
