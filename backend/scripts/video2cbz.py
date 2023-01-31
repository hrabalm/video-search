#!/usr/bin/env python

import cbz
import click
from indexing import read_frames
from utils import time_exec


@click.command()
@click.argument("input_filename")
@click.argument("output_filename")
def video2cbz(input_filename: str, output_filename: str):
    @time_exec
    def f():
        frames = read_frames(input_filename)
        images = map(lambda frame: frame.to_image(), frames)
        with open(output_filename, "wb") as f:
            cbz.save_images_to_zipfile(images, f)

    took, _ = f()
    print(f"Convertsion took {took/10**9}s")


if __name__ == "__main__":
    video2cbz()
