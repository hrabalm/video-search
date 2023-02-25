import logging
import pathlib
from itertools import chain

import backend.models
import backend.tagging
from backend.classifiers.prediction import Video


def process_file(file: pathlib.Path):
    import backend.tagging
    import backend.tagging.perframe

    def load_efficientnet():
        import backend.classifiers.efficientnet as efficientnet

        return efficientnet.EfficientNetClassifier()

    processors: list[backend.tagging.IVideoProcessor] = [
        backend.tagging.VideoTaggerRunner(
            taggers=[
                lambda: backend.tagging.perframe.VideoPerFrameTagger(
                    "tf-efficientnet", load_efficientnet
                ),
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
                # logging.error(str(e))  # FIXME: FORMAT
                logging.exception(e)
        backend.models.Videos.insert_one(video.dict())
