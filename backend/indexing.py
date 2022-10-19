import typing
from collections import defaultdict
from typing import Collection, Iterable

import av
import PIL.Image
from more_itertools import ichunked
from pydantic import BaseModel
from simple_file_checksum import get_checksum
from toolz import concat, count

from classifiers import AbstractClassifier
from classifiers.prediction import GroupedPrediction, Prediction


class FileHash(BaseModel):
    filename: str
    hash_function: str
    checksum: str


class DecodedFrame(BaseModel):
    image: PIL.Image.Image
    pts: int

    class Config:
        arbitrary_types_allowed = True


def file_hash(filename, hash_function="SHA256") -> FileHash:
    checksum = get_checksum(filename, hash_function)
    return FileHash(
        filename=filename,
        hash_function=hash_function,
        checksum=checksum,
    )


def read_frames(file: str | typing.BinaryIO, keyframes_only=False):
    with av.open(file) as container:
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        if keyframes_only:
            stream.codec_context.skip_frame = "NONKEY"
        for frame in container.decode(stream):
            yield frame


def resize_frame(frame, resolution) -> DecodedFrame:
    return DecodedFrame(
        image=frame.to_image().convert("RGB").resize(resolution), pts=frame.pts
    )


def read_frames_resized(
    file: str | typing.BinaryIO, resolution: tuple[int, int], keyframes_only=False
):
    return map(
        lambda frame: resize_frame(frame, resolution),
        read_frames(file, keyframes_only=keyframes_only),
    )


def count_keyframes(filename) -> int:
    return count(read_frames(filename, keyframes_only=True))


def classify_chunks(chunks, classifier: AbstractClassifier):
    def classify_chunk(chunk: Iterable[DecodedFrame]):
        chunk = list(chunk)
        images = map(lambda f: f.image, chunk)
        pts = map(lambda f: f.pts, chunk)
        predictions = classifier.classify_batch(list(images))
        predictions_with_pts = [
            Prediction(score=pred.score, label=pred.label, pts=pred_pts)
            for pred, pred_pts in zip(predictions, pts)
        ]
        return predictions_with_pts

    classified_chunks = list(map(classify_chunk, chunks))
    classified_frames = list(concat(classified_chunks))
    return classified_frames


def index_video_file(filename: str | typing.BinaryIO, classifier: AbstractClassifier):
    _ = tag_video_file(filename, classifier)
    raise NotImplementedError


def combine_labels(labels):
    return labels


def group_predictions(
    predictions: Collection[Prediction],
) -> Collection[GroupedPrediction]:
    predictions_by_label = defaultdict(lambda: [])

    for prediction in predictions:
        predictions_by_label[prediction.label].append(prediction)

    return [
        GroupedPrediction(label=label, predictions=predictions_by_label[label])
        for label in predictions_by_label
    ]


def tag_video(
    file: str | typing.BinaryIO,
    classifier: AbstractClassifier,
    chunk_size: int = 1000,
    keyframes_only=False,
):
    frames = read_frames_resized(file, (224, 224), keyframes_only)
    frame_chunks = ichunked(frames, chunk_size)
    classified_frames = classify_chunks(frame_chunks, classifier)
    video_tags = combine_labels(classified_frames)
    return video_tags


def tag_video_file(
    filename,
    classifier: AbstractClassifier,
    chunk_size: int = 1000,
    keyframes_only=False,
):
    with open(filename, "rb") as f:
        return tag_video(f, classifier, chunk_size, keyframes_only)


def select_tags(predictions: list[Prediction], min_score):
    return list(
        filter(
            lambda pred: pred.score >= min_score,
            predictions,
        )
    )


def group_tags(predictions: list[Prediction]) -> dict[str, Prediction]:
    predictions_by_label = defaultdict(lambda: [])
    for pred in predictions:
        predictions_by_label[pred.label].append(pred)
    return dict(predictions_by_label)


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


if __name__ == "__main__":
    pass
    # tests
    # raw_results = tag_video_file(
    #     "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4",
    #     EfficientNetClassifier(),
    # )
    # # print(tags)

    # import pickle

    # # with open("raw_results.pickle", "wb") as f:
    # #     pickle.dump(raw_results, f)

    # from collections import defaultdict

    # unique_tags = set()
    # histogram = defaultdict(lambda: 0)
    # max_conf = defaultdict(lambda: 0.0)

    # # filtered_tags = filter(lambda tag: tag[0][2] > 0.5, tags)

    # # all_tags = set(tag[0][1] for tag in filtered_tags)
    # # print(all_tags)

    # for tag in raw_results:
    #     _, name, conf = tag[0]
    #     unique_tags.add(name)
    #     histogram[name] += 1
    #     max_conf[name] = max(max_conf[name], conf)

    # results = [(max_conf[name], histogram[name], name) for name in unique_tags]
    # print(results)
