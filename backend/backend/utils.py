import functools
import time
from pathlib import Path
from typing import Any, Callable


def time_exec(f) -> Callable[..., tuple[float, Any]]:
    functools.wraps(f)

    def wrapper():
        start = time.time_ns()
        res = f()
        end = time.time_ns()
        return end - start, res

    return wrapper


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def annote_image(image, text: str):
    import PIL.Image
    import PIL.ImageDraw
    import PIL.ImageFont

    try:
        font = PIL.ImageFont.truetype("DejaVuSans.ttf", 32)
    except OSError:
        font = PIL.ImageFont.load_default()
    draw = PIL.ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font, fill=(225, 0, 0))
    return image
