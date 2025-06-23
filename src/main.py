from map import generate_map
from map_editor import run_interactive_map
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="path to directory with all of the necessary files")
    parser.add_argument("--font_path", default="../fonts/alegreya/ttf/Alegreya-Regular.ttf", help="path to font file RELATIVE to --dir")
    parser.add_argument("-i", action="store_true", help="enables interactive mode")
    parser.add_argument("--draw_offsets", action="store_true", help="enables the drawing of offset lines")
    parser.add_argument("--omit_battue_names", action="store_true", help="disables the drawing of battue names")
    args = parser.parse_args()
    paths = {}
    paths["font"] = args.font_path
    paths["map_image"] = "base_map.png"
    paths["map_output"] = "new_map.png"
    paths["postes_csv"] = "postes.csv"
    paths["gps_file"] = "gps.json"
    paths["battues"] = "battues.json"
    for key, val in paths.items():
        paths[key] = os.path.join(args.dir, val)

    if args.i:
        run_interactive_map(paths, draw_offsets=args.draw_offsets, draw_battue_names=not args.omit_battue_names)
    else:
        generate_map(paths, draw_offsets=args.draw_offsets, draw_battue_names=not args.omit_battue_names)


if __name__ == "__main__":
    main()
