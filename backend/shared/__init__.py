from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, NamedTuple, Tuple, TypedDict, cast

import bson
import lz4.block
from PIL import Image

RawImage = bytes
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


@dataclass
class ImageRecognitionRequest:
    """A wrapper around a single image that is to be tagged."""

    image: Image.Image

    def tobytes(self) -> bytes:
        size = self.image.size
        image_bytes = self.image.tobytes()
        image_format = cast(ColorMode, self.image.mode)
        uncompressed = bson.encode(
            ImageRecognitionRequest._ImageRequestTD(
                size=size, image_bytes=image_bytes, image_format=image_format
            )
        )
        compressed = lz4.block.compress(uncompressed)

        return compressed

    class ImageRecognitionRequestTD(TypedDict):
        pass

    def todict(self) -> ImageRecognitionRequestTD:
        return ImageRecognitionRequest.ImageRecognitionRequestTD()

    @staticmethod
    def fromdict(
        x: ImageRecognitionRequest.ImageRecognitionRequestTD,
    ) -> ImageRecognitionRequest:
        raise NotImplementedError

    @staticmethod
    def frombytes(data) -> ImageRecognitionRequest:
        decompressed = lz4.block.decompress(data)
        decoded = bson.decode(decompressed)
        typed = cast(ImageRecognitionRequest._ImageRequestTD, decoded)
        img = Image.frombytes(
            typed["image_format"],
            typed["size"],
            typed["image_bytes"],
        )

        return ImageRecognitionRequest(img)

    class _ImageRequestTD(TypedDict):
        size: Tuple[int, int]
        image_format: ColorMode
        image_bytes: RawImage
        # TODO: I should probably add something like this:
        # image_uid: str   # what video?
        # image_frame: int # what frame?
        # image_frames_total: int  # how many frames are there in total? redundant,
        # but small


@dataclass
class ImageRecognitionRequestBatch:
    requests: list[ImageRecognitionRequest]

    def to_bytes(self, compression=None):
        raise NotImplementedError

    @staticmethod
    def from_bytes(x: bytes):
        raise NotImplementedError

    def to_bson(self):
        raise NotImplementedError

    @staticmethod
    def from_bson(x):  # FIXME: type annotation
        raise NotImplementedError


class Tag(NamedTuple):
    id: str
    name: str
    conf: float
    source: str


@dataclass
class ImageTags:
    tags: List[Tag]
