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
        uncompressed = bson.encode(self.to_dict())
        compressed = lz4.block.compress(uncompressed)

        return compressed

    def to_dict(self) -> _ImageRecognitionRequestTD:
        return ImageRecognitionRequest._ImageRecognitionRequestTD(
            size=self.image.size,
            image_format=cast(ColorMode, self.image.mode),
            image_bytes=self.image.tobytes(),
        )

    @staticmethod
    def from_dict(
        x: ImageRecognitionRequest._ImageRecognitionRequestTD,
    ) -> ImageRecognitionRequest:
        mode = x["image_format"]
        size = x["size"]
        data = x["image_bytes"]
        image = Image.frombytes(mode, size, data)

        return ImageRecognitionRequest(image)

    @staticmethod
    def frombytes(data) -> ImageRecognitionRequest:
        decompressed = lz4.block.decompress(data)
        decoded = bson.decode(decompressed)
        typed = cast(ImageRecognitionRequest._ImageRecognitionRequestTD, decoded)
        img = Image.frombytes(
            typed["image_format"],
            typed["size"],
            typed["image_bytes"],
        )

        return ImageRecognitionRequest(img)

    class _ImageRecognitionRequestTD(TypedDict):
        size: Tuple[int, int]
        image_format: ColorMode
        image_bytes: RawImage
        # TODO: I should probably add something like this:
        # image_uid: str   # what video?
        # image_frame: int # what frame?
        # image_frames_total: int  # how many frames are there in total? redundant,
        # but small


compress = {"lz4": lz4.block.compress}

decompress = {"lz4": lz4.block.decompress}


@dataclass
class ImageRecognitionRequestBatch:
    requests: list[ImageRecognitionRequest]

    def to_bytes(self, compression=None) -> bytes:
        body = {"requests": [request.to_dict() for request in self.requests]}
        encoded_body = bson.encode(body)
        if compression:
            encoded_body = compress[compression](encoded_body)

        serialization = {
            "compression": compression,
            "body": encoded_body,
        }

        serialization = bson.encode(serialization)

        return serialization

    @staticmethod
    def from_bytes(x: bytes):
        serialization = bson.decode(x)

        body = serialization["body"]
        if serialization["compression"]:
            compression = serialization["compression"]
            body = decompress[compression](serialization["body"])

        requests_dicts: list[
            ImageRecognitionRequest._ImageRecognitionRequestTD
        ] = bson.decode(body)["requests"]
        requests = [
            ImageRecognitionRequest.from_dict(request) for request in requests_dicts
        ]

        return ImageRecognitionRequestBatch(requests)

    # def to_bson(self):
    #     raise NotImplementedError

    # @staticmethod
    # def from_bson(x):  # FIXME: type annotation
    #     raise NotImplementedError


class Tag(NamedTuple):
    id: str
    name: str
    conf: float
    source: str


@dataclass
class ImageTags:
    tags: List[Tag]
