import io
import pickle
import typing
import zipfile
from multiprocessing import Pool
from typing import Collection, Iterable

from PIL.Image import Image


def convert_to_png(image: Image) -> bytes:
    with io.BytesIO() as out_f:
        image.save(out_f, "png")

        return out_f.getvalue()


def save_images_to_zipfile(images: Iterable[Image], f: typing.BinaryIO, verbose=False):
    with Pool() as p:
        png_images = p.imap(
            convert_to_png,
            images,
        )
        with zipfile.ZipFile(f, mode="w", compression=zipfile.ZIP_STORED) as zf:
            for i, image in enumerate(png_images):
                filename = f"{i:09}.png"
                if verbose:
                    print(f"Adding {filename}...")
                zf.writestr(filename, image)


def save_images_to_zipfile_in_memory(images: Collection[Image]):
    with io.BytesIO() as f:
        save_images_to_zipfile(images, f)
        return f.getvalue()


def pickle_to_zip(input_filemame, output_filename):
    with open(input_filemame, "rb") as in_f:
        images = pickle.load(in_f)
    zipbytes = save_images_to_zipfile_in_memory(images)
    with open(output_filename, "wb") as out_f:
        out_f.write(zipbytes)
