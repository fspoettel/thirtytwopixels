#!/usr/bin/env python3
import argparse
from client.matrix import Matrix

parser = argparse.ArgumentParser(description="CLI to manually send messages tot thirtytwopixels")
parser.add_argument("command", nargs="?")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.command == "clear":
        matrix = Matrix([32, 32])
        matrix.clear()
    else:
        print("unknown command: {}".format(args.command))
