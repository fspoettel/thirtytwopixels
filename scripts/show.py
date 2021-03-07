#!/usr/bin/env python3
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import argparse
from pathlib import Path
from client.matrix_connection import MatrixConnection

parser = argparse.ArgumentParser(description="CLI to manually send messages tot thirtytwopixels")
parser.add_argument("image")

if __name__ == "__main__":
    args = parser.parse_args()
    matrix = MatrixConnection([32, 32])
    img_path = Path(args.image)

    if img_path.is_file():
        matrix.show(img_path)
    else:
        print("could not read image file")
