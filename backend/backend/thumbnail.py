import io
import pathlib

from PIL import Image

from backend.tagging.perframe import count_keyframes, read_frames


def _select_keyframe_indices(count: int, target_count):
    # FIXME: sometimes off by one?
    indices = list(range(0, count, count // (target_count + 1)))[1:-1]
    return indices


def _select_keyframes(keyframes, indices: set[int]):
    for i, frame in enumerate(keyframes):
        if i in indices:
            yield frame


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

    count = count_keyframes(str(filepath))
    frames = read_frames(str(filepath), keyframes_only=True)
    indices = _select_keyframe_indices(count, thumbnails_count)

    selected_frames = _select_keyframes(frames, set(indices))
    thumbnails = (
        _to_webp(_resize(frame.to_image(), max_width, max_height))
        for frame in selected_frames
    )

    return thumbnails
