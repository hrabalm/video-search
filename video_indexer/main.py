import argparse
import indexer

HOST = "localhost"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("filename")

    args = parser.parse_args()

    with open(args.filename, "rb") as file:
        indexer.process_video(file)
