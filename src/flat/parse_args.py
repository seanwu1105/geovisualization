import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--geometry", default="assets/elevation_small.vti")
    parser.add_argument(
        "-i", "--image", default="assets/world.topo.bathy.200408.medium.jpg"
    )

    return parser.parse_args()
