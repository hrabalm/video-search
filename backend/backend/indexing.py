import typing
from collections import defaultdict
from typing import Collection, Iterable, Iterator

import av
import PIL.Image
from more_itertools import ichunked
from pydantic import BaseModel
from toolz import concat, count

from backend.classifiers import AbstractClassifier
from backend.classifiers.prediction import (
    GroupedPerFramePrediction,
    PerFramePrediction,
    VideoTag,
)


class DecodedFrame(BaseModel):
    image: PIL.Image.Image
    pts: int

    class Config:
        arbitrary_types_allowed = True


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
            [
                PerFramePrediction(score=pred.score, label=pred.label, pts=pred_pts)
                for pred in preds
            ]
            for preds, pred_pts in zip(predictions, pts)
        ]
        predictions_with_pts_flat = concat(predictions_with_pts)
        return predictions_with_pts_flat

    classified_chunks = list(map(classify_chunk, chunks))
    classified_frames = list(concat(classified_chunks))
    return classified_frames


def group_predictions(
    predictions: Collection[PerFramePrediction],
) -> Collection[GroupedPerFramePrediction]:
    predictions_by_label = defaultdict(lambda: [])

    for prediction in predictions:
        predictions_by_label[prediction.label].append(prediction)

    return [
        GroupedPerFramePrediction(label=label, predictions=predictions_by_label[label])
        for label in predictions_by_label
    ]


def add_best_frames_for_grouped_predictions(
    video_file, groups: Collection[GroupedPerFramePrediction]
) -> Iterator[tuple[GroupedPerFramePrediction, PIL.Image.Image]]:
    """Goes through a collection of groups and for each finds the frame that
    was classified with the greatest confidence.

    GroupedPredictions are yielded lazily so that all images don't have to be
    loaded to the memory at the same time."""

    def get_frame_index(group: GroupedPerFramePrediction):
        best_pred = max(group.predictions, key=lambda pred: pred.score)
        if best_pred.pts is not None:
            return best_pred.pts
        else:
            raise ValueError(f"Missing pts for {best_pred}")

    frame_pts = sorted(list(map(get_frame_index, groups)))
    groups_by_pts = {get_frame_index(g): g for g in groups}

    for frame in read_frames(video_file):
        if frame.pts in frame_pts:
            yield groups_by_pts[frame.pts], frame.to_image()


def create_video_tags(
    file, model: str, grouped_predictions: Collection[GroupedPerFramePrediction]
) -> Iterator[VideoTag]:
    for group in grouped_predictions:
        frame_pts = group.best().pts
        yield VideoTag(
            model=model,
            tag=group.label,
            frame_pts=([frame_pts] if frame_pts else []),
            conf=group.best_score(),
        )


def tag_video(
    file: str | typing.BinaryIO,
    classifier: AbstractClassifier,
    chunk_size: int = 1000,
    keyframes_only=False,
):
    frames = read_frames_resized(file, classifier.required_resolution, keyframes_only)
    frame_chunks = ichunked(frames, chunk_size)
    classified_frames = classify_chunks(frame_chunks, classifier)
    grouped_predictions = group_predictions(classified_frames)
    video_tags = create_video_tags(file, str(classifier), grouped_predictions)
    return video_tags


def select_tags(predictions: list[PerFramePrediction], min_score):
    return list(
        filter(
            lambda pred: pred.score >= min_score,
            predictions,
        )
    )


def group_tags(predictions: list[PerFramePrediction]) -> dict[str, PerFramePrediction]:
    predictions_by_label = defaultdict(lambda: [])
    for pred in predictions:
        predictions_by_label[pred.label].append(pred)
    return dict(predictions_by_label)


if __name__ == "__main__":
    pass
