#!/usr/bin/env python3
import argparse
from pathlib import Path
from client.matrix import Matrix

parser = argparse.ArgumentParser(description="CLI to manually send messages tot thirtytwopixels")
parser.add_argument("image")

if __name__ == "__main__":
    args = parser.parse_args()
    matrix = Matrix([32, 32])
    img_path = Path(args.image)

    if img_path.is_file():
        matrix.show(img_path)
    else:
        print("could not read image file")
