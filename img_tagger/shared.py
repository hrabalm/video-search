from __future__ import annotations

import collections
from dataclasses import dataclass
from typing import NamedTuple, TypedDict, cast, Tuple

import bson
from pika import connection
from PIL import Image


class _ImageRequestTD(TypedDict):
    size: Tuple[int, int]
    image_format: str
    image_bytes: bytes


class ImageRequest:
    def __init__(self, img: Image.Image):
        self.img: Image.Image = img

    def tobytes(self) -> bytes:
        size = self.img.size
        image_bytes = self.img.tobytes()
        image_format = self.img.mode

        return bson.dumps(_ImageRequestTD(size=size, image_bytes=image_bytes, image_format=image_format))

    @staticmethod
    def frombytes(data) -> ImageRequest:
        decoded = bson.loads(data)
        typed = cast(_ImageRequestTD, decoded)
        img = Image.frombytes(typed['image_format'],
                              typed['size'], typed['image_bytes'])

        return ImageRequest(img)


VideoTag1 = collections.namedtuple('VideoTag1', ['tag', 'confidence'])


@dataclass
class VideoTag2():
    tag: str
    confidence: float
    source: str
