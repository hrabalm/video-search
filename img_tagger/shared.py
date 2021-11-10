from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, TypedDict

import bson
from PIL import Image


class _ImageRequestTD(TypedDict):
    size: int
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
        typed = _ImageRequestTD(decoded)
        img = Image.frombytes(typed['image_format'],
                              typed['size'], typed['image_bytes'])

        return ImageRequest(img)
