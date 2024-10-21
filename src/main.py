from map import generate_map
from map_editor import run_interactive_map
import os


def main():
    base_path = "../content/st-leger/"
    paths = {}
    paths["font"] = "BebasNeue-Regular.ttf"
    paths["map_image"] = "saint-leger.png"
    paths["map_output"] = "new_map.png"
    paths["postes_csv"] = "postes.csv"
    paths["gps_file"] = "saint-leger.json"
    paths["battues"] = "battues.json"
    for key, val in paths.items():
        paths[key] = os.path.join(base_path, val)

    # generate_map(paths)
    run_interactive_map(paths)


if __name__ == "__main__":
    main()
