import pathlib
import typing
from collections import defaultdict
from itertools import chain
from typing import Collection, Iterable, Iterator
import logging

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


def process_file(file: pathlib.Path):
    import backend.tagging
    import backend.tagging.perframe

    def load_efficientnet():
        import backend.classifiers.efficientnet as efficientnet
        return efficientnet.EfficientNetClassifier()

    processors: list[backend.tagging.IVideoProcessor] = [
        backend.tagging.VideoTaggerRunner(
            taggers=[
                lambda: backend.tagging.perframe.VideoPerFrameTagger("tf-efficientnet", load_efficientnet),
            ]
        )
    ]
    indexer = VideoIndexer(processors)
    indexer.index_video(file)


def is_video_file(file: pathlib.Path, extensions: set[str]):
    return file.is_file() and str.lower(file.suffix) in extensions


def find_video_files(directories: list[str], extensions: list[str]):
    extensions_set = set(extensions)
    directories_set = [pathlib.Path(d) for d in directories]
    assert all(d.is_dir() for d in directories_set)

    video_files = filter(
        lambda f: is_video_file(f, extensions_set),
        chain.from_iterable(d.glob("**/*") for d in directories_set),
    )

    return video_files


def delete_index():
    from backend.api.db import db_videos

    db_videos.delete_many({})


def reindex_all(directories: list[str], extensions: list[str]):
    delete_index()
    files = find_video_files(directories, extensions)

    # TODO: Process multiple files at once
    # with multiprocessing.Pool(1) as p:
    # p.map(process_file, files)
    list(map(process_file, files))


# indexing
import backend.models
import backend.tagging
from backend.classifiers.prediction import Video, VideoTag


class VideoIndexer:
    def __init__(self, video_processors: list[backend.tagging.IVideoProcessor]):
        self.processors = video_processors

    def index_video(self, path: pathlib.Path):
        # TODO: only update old/missing if not exists
        video = Video(filenames=[str(path)], filehash="NotImplemented", tags=[])
        for processor in self.processors:
            try:
                # TODO: only necessary if missing/old (in which case I should)
                # remove old data first
                video = processor.process(video, path)
            except Exception as e:
                logging.error(str(e))  # FIXME: FORMAT
        backend.models.Videos.insert_one(video.dict())
