import io
import pathlib

from PIL import Image

from backend.video_reader import get_frames_by_pts_approximate, max_pts


def _sample_pts(filepath: pathlib.Path, count: int) -> list[int]:
    """Try to uniformly select `count` pts to cover the video."""
    max_pts_value = max_pts(filepath)
    sampled_pts = [i * max_pts_value // (count + 1) for i in range(1, count + 1)]
    print(sampled_pts)
    return sampled_pts


def _select_frames(filepath: pathlib.Path, sample_pts: list[int], keyframes_only=True):
    """Return frames which approximately match given pts."""
    frames = list(get_frames_by_pts_approximate(filepath, sample_pts, keyframes_only))

    return frames


def _downsize_dimensions(width, height, max_width, max_height):
    ratio = min(width / max_width, height / max_height, 1.0)

    return round(width * ratio), round(height * ratio)


def _resize(image: Image.Image, max_width, max_height):
    current_width = image.width
    current_height = image.height

    target_width, target_height = _downsize_dimensions(
        current_width, current_height, max_width, max_height
    )
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)


def _to_webp(image: Image.Image):
    with io.BytesIO() as f:
        image.save(f, "webp")
        return f.getvalue()


def create_thumbnails(
    filepath: pathlib.Path, thumbnails_count: int, max_width: int, max_height: int
):
    assert filepath.exists()
    assert filepath.is_file()

    selected_frames = _select_frames(
        filepath, _sample_pts(filepath, thumbnails_count), keyframes_only=True
    )
    thumbnails = (
        _to_webp(_resize(frame.to_image(), max_width, max_height))
        for frame in selected_frames
    )

    return thumbnails
