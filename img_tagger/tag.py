from dataclasses import dataclass
from typing import TypedDict


@dataclass
class ImageTag:
    decoded_preds: dict


# TOOD: Maybe remove
class TagV1(TypedDict):
    pass
