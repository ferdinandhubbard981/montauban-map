from map import Map
from battue import Battue
import json


def main():
    map = Map("../content/saint-leger.png", "../content/saint-leger.json")
    print(f"longitude_pixel_delta: {map.longitude_pixel_delta}")
    file = open("../content/battues.json", "r")
    json_content = json.load(file)
    file.close()
    for battue_json in json_content:
        battue = Battue(battue_json)
        print(f"{battue.name} postes len: {len(battue.postes)}")


if __name__ == "__main__":
    main()
