# mock image

from __future__ import annotations

import io
import pickle
import random
from typing import BinaryIO, Iterable

import av
import lz4.frame
from PIL import Image


def mock_empty_image(size=(224, 224)) -> Image.Image:
    return Image.new("RGB", size)


def take_random_frames(video_file, count) -> list[Image.Image]:
    def count_frames(container):
        counter = 0
        for _ in container.decode(video=0):
            counter += 1
        return counter

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


class VideoFramesProducerMockWithPool:
    """Produces testing images from a pool of list of images."""

    def __init__(self, pool: list[Image.Image]):
        self.pool = pool

    def take(self, n: int):
        if n > len(self.pool):
            raise Exception("Pool is smaller than requiered count of elements.")
        return self.pool[:n]

    @staticmethod
    def load(fileobj: BinaryIO) -> VideoFramesProducerMockWithPool:
        def from_png(x: bytes):
            with io.BytesIO(x) as f:
                return Image.open(f)

        compressed = fileobj.read()
        pickled = lz4.frame.decompress(compressed)
        unpickled = pickle.loads(pickled)
        loaded = [from_png(image) for image in unpickled]

        return VideoFramesProducerMockWithPool(loaded)

    def save(self, fileobj: BinaryIO):
        def to_png(image: Image.Image):
            with io.BytesIO() as f:
                image.save(f, "PNG")
                return f.getvalue()

        pool = [to_png(image) for image in self.pool]
        pickled = pickle.dumps(pool)
        compressed = lz4.frame.compress(pickled)
        fileobj.write(compressed)

    @staticmethod
    def from_video_file(
        filename: str, pool_size=1024, size=(224, 224)
    ) -> VideoFramesProducerMockWithPool:
        """Created from a given video file. Requires that all decoded and
        resized frames fit into memory at the same time."""
        frames = []
        for i, frame in enumerate(av.open(filename).decode(video=0)):
            # maybe use different resize technique to save time?
            # (bicubic by default)
            image = frame.to_image().convert("RGB").resize(size)
            frames.append(image)

            if i > 10 * pool_size:
                # Don't read the whole video
                break
        print(f"{len(frames)=}")
        selected = random.choices(frames, k=pool_size)
        print(f"{len(selected)=}")

        return VideoFramesProducerMockWithPool(selected)


if __name__ == "__main__":
    p = VideoFramesProducerMockWithPool.from_video_file(
        "[HorribleSubs] Machikado Mazoku - 02 [1080p].mkv",
        pool_size=256,
    )
    with open("frames.pickle", "wb") as f:
        p.save(f)


# mock requests, jobs, responses
# mock video
