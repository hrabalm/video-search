# mock image

from typing import Iterable

from PIL import Image


def mock_empty_image(size=(224, 224)) -> Image.Image:
    return Image.new("RGB", size)


def take_random_frames(video_file, count) -> list[Image.Image]:
    def count_frames(container):
        counter = 0
        for _ in container.decode(video=0):
            counter += 1
        return counter

    import random

    import av

    random.seed(42)
    container = av.open(video_file)
    # frames_count = container.streams.video[0].frames
    frames_count = count_frames(container)
    print(f"{frames_count=}")
    selected_frames_indices = set(random.choices(range(frames_count), k=count))
    selected_frames = []
    container.seek(0)
    frames = container.decode(video=0)
    for i, frame in enumerate(frames):
        if i in selected_frames_indices:
            selected_frames.append(frame.to_image().resize((224, 224)))
    return selected_frames


class VideoFramesProducerMock:
    """Produces testing images."""

    def __init__(self, width: int = 224, height: int = 224, sample_size=1000):
        self.width = width
        self.height = height

        self._batch = [mock_empty_image() for _ in range(sample_size)]

    def take(self) -> Iterable[Image.Image]:
        return self._batch


# mock requests, jobs, responses
# mock video
