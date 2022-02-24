from __future__ import annotations

import collections
from dataclasses import dataclass
from typing import List, Literal, NamedTuple, Tuple, TypedDict, cast

import bson
import lz4.block
from PIL import Image

ColorMode = Literal[
    "1",
    "CMYK",
    "F",
    "HSV",
    "I",
    "L",
    "LAB",
    "P",
    "RGB",
    "RGBA",
    "RGBX",
    "YCbCr",
]


class _ImageRequestTD(TypedDict):
    size: Tuple[int, int]
    image_format: ColorMode
    image_bytes: bytes
    # TODO: I should probably add something like this:
    # image_uid: str   # what video?
    # image_frame: int # what frame?
    # image_frames_total: int  # how many frames are there in total? redundant,
    # but small


class ImageRequest:
    def __init__(self, img: Image.Image):
        self.img: Image.Image = img

    def tobytes(self) -> bytes:
        size = self.img.size
        image_bytes = self.img.tobytes()
        image_format = cast(ColorMode, self.img.mode)
        uncompressed = bson.dumps(
            _ImageRequestTD(
                size=size, image_bytes=image_bytes, image_format=image_format
            )
        )
        compressed = lz4.block.compress(uncompressed)

        return compressed

    @staticmethod
    def frombytes(data) -> ImageRequest:
        decompressed = lz4.block.decompress(data)
        decoded = bson.loads(decompressed)
        typed = cast(_ImageRequestTD, decoded)
        img = Image.frombytes(
            typed["image_format"],
            typed["size"],
            typed["image_bytes"],
        )

        return ImageRequest(img)


class Tag(NamedTuple):
    id: str
    name: str
    conf: float
    source: str


@dataclass
class ImageTag:
    tags: List[Tag]


class VideoTag:
    tags: List[VideoTag]


VideoTag1 = collections.namedtuple("VideoTag1", ["tag", "confidence"])


@dataclass
class VideoTag2:
    tag: str
    confidence: float
    source: str
