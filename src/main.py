from map import Map


def main():
    map = Map("../content/saint-leger.png", "../content/saint-leger.json")
    print(map.longitude_pixel_delta)


if __name__ == "__main__":
    main()
