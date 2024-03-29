import base64
import io
from typing import Any, Optional

import PIL.Image
from bson.codec_options import CodecOptions, TypeCodec, TypeRegistry
from pydantic import BaseModel, validator


class PerFramePrediction(BaseModel):
    """Output for models that classify models in isolation."""

    score: float
    label: str
    pts: Optional[int] = None


class GroupedPerFramePrediction(BaseModel):
    label: str
    predictions: list[PerFramePrediction]

    def count(self) -> int:
        return len(self.predictions)

    def best(self) -> PerFramePrediction:
        return max(self.predictions, key=lambda p: p.score)

    def best_score(self) -> float:
        return self.best().score


def _save_image_to_png_bytes(img: PIL.Image.Image) -> bytes:
    f = io.BytesIO()
    img.save(f, format="png")
    return f.getvalue()


def _save_image_to_png_str(img: PIL.Image.Image) -> str:
    return base64.b64encode(_save_image_to_png_bytes(img)).decode("utf-8")


def _load_image_from_png_bytes(b: bytes) -> PIL.Image.Image:
    f = io.BytesIO(b)
    img = PIL.Image.open(f)
    return img


def _load_image_from_png_str(s: str) -> PIL.Image.Image:
    return _load_image_from_png_bytes(base64.b64decode(s))


# FIXME: deserialization
class WrappedImage(BaseModel):
    image: PIL.Image.Image

    @validator("image", pre=True)
    def parse_image(cls, value):
        if isinstance(value, PIL.Image.Image):
            return value
        if isinstance(value, str):
            return _load_image_from_png_str(value)
        if isinstance(value, bytes):
            return _load_image_from_png_bytes(value)

    @classmethod
    def validate(cls, v):
        return v

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PIL.Image.Image: _save_image_to_png_str}


class SourceFrameReference(BaseModel):
    video_filename: str
    video_hash: str
    pts: int


class VideoTag(BaseModel):
    model: str
    tag: str
    frame_pts: list[int] = []
    conf: float

    class Config:
        arbitrary_types_allowed = True


class Video(BaseModel):
    filenames: list[str]
    filehash: str
    thumbnails: list[str] = []
    tags: list[VideoTag]


class ImageCodec(TypeCodec):
    python_type = PIL.Image.Image  # type: ignore
    bson_type = bytes  # type: ignore

    def transform_python(self, value: Any) -> Any:
        return _save_image_to_png_bytes(value)

    def transform_bson(self, value: Any) -> Any:
        return _load_image_from_png_bytes(value)


type_registry = TypeRegistry([ImageCodec()])
codec_options = CodecOptions(type_registry=type_registry)
