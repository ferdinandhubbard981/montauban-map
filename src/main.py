from map import Map
from battue import Battue
import json


def main():
    map = Map("../content/saint-leger.png", "../content/saint-leger.json")
    print(f"x_pixel_delta: {map.x_pixel_delta}")
    file = open("../content/battues.json", "r")
    json_content = json.load(file)
    file.close()
    battues = []
    for battue_json in json_content:
        battue = Battue(battue_json)
        battues.append(battue)
        map.draw_line(battue)
        map.draw_postes(battue)
        map.draw_battue_name(battue)
        print(f"{battue.name} postes len: {len(battue.postes)}")
    map.image.show()
    map.image.save("../content/new_map.png")


if __name__ == "__main__":
    main()
