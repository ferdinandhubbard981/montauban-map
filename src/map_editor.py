import cv2
from map import generate_map
from util import pixel_distance, parse_optional_int_to_str
import numpy as np
import csv

selected_poste = None


def load_map(paths):
    map_data, battues = generate_map(paths, draw_offsets=True)
    img = cv2.imread(paths["map_output"])
    cv2.imshow('window', img)
    params = (map_data, battues, paths)
    cv2.setMouseCallback('window', click_event, params)


def run_interactive_map(paths):
    cv2.namedWindow("window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("window", 1920, 1080)
    load_map(paths)
    while 1:
        key = cv2.waitKey(0)
        if key == 27:
            break
        if key == ord('r'):
            load_map()

    cv2.destroyAllWindows()


def click_event(event, x, y, flags, params):
    global selected_poste
    map_data = params[0]
    battues = params[1]
    paths = params[2]
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Coordinates: ({x}, {y})')
        if flags & cv2.EVENT_FLAG_SHIFTKEY and selected_poste is not None:
            print("updating csv...")
            selected_poste_pixel = map_data.convert_lambert_to_pixel(selected_poste.lambert_point)
            selected_poste_pixel += selected_poste.line_offset
            # calculate pixel offset and apply to current poste in csv
            pixel_offset = np.array([x, y]) - selected_poste_pixel
            pixel_offset = np.rint(pixel_offset).astype(np.int32)
            print(f"moving {selected_poste.battue_name} {selected_poste.number} by ({pixel_offset[0]}, {pixel_offset[1]}) pixels")
            # find entry for that poste
            rows = []
            with open(params["postes_csv"], 'r') as csvfile:
                data_reader = csv.DictReader(csvfile, delimiter=';')
                rows.append(data_reader.fieldnames)
                for row in data_reader:
                    if row["name"] == selected_poste.number and row["battue"] == selected_poste.battue_name:
                        row["line_offset_x"] = str(parse_optional_int_to_str(row["line_offset_x"]) + pixel_offset[0])
                        row["line_offset_y"] = str(parse_optional_int_to_str(row["line_offset_y"]) + pixel_offset[1])
                    rows.append(list(row.values()))

            with open(params["postes_csv"], 'w') as csvfile:
                data_writer = csv.writer(csvfile, delimiter=';')
                data_writer.writerows(rows)

            # modify offsets
            selected_poste = None
        else:
            nearest_poste = None
            nearest_poste_distance = 0
            for battue in battues:
                for poste in battue.postes:
                    distance = pixel_distance(map_data.convert_lambert_to_pixel(poste.lambert_point) + poste.line_offset, np.array([x, y]))
                    if nearest_poste is None or distance < nearest_poste_distance:
                        nearest_poste = poste
                        nearest_poste_distance = distance
            selected_poste = nearest_poste
            print(f"selected poste: {selected_poste.battue_name} {selected_poste.number}")
            # cv2.imshow('image', img)
