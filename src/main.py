from map import generate_map
from map_editor import run_interactive_map
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="path to directory with all of the necessary files")
    parser.add_argument("-i", action="store_true", help="path to directory with all of the necessary files")
    parser.add_argument("--draw_offsets", action="store_true", help="path to directory with all of the necessary files")
    args = parser.parse_args()
    paths = {}
    paths["font"] = "../fonts/alegreya/ttf/Alegreya-Bold.ttf"
    paths["map_image"] = "base_map.png"
    paths["map_output"] = "new_map.png"
    paths["postes_csv"] = "postes.csv"
    paths["gps_file"] = "gps.json"
    paths["battues"] = "battues.json"
    for key, val in paths.items():
        paths[key] = os.path.join(args.dir, val)

    if args.i:
        run_interactive_map(paths)
    else:
        generate_map(paths, draw_offsets=args.draw_offsets)


if __name__ == "__main__":
    main()
