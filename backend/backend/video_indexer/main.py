import argparse

import backend.video_indexer.indexer

HOST = "localhost"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("filename")

    args = parser.parse_args()

    with open(args.filename, "rb") as file:
        backend.video_indexer.indexer.process_video(file)
