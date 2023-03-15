import concurrent.futures
import logging
import pathlib
from itertools import chain

import backend.models
import backend.tagging
import backend.utils as utils
from backend.classifiers.prediction import Video
from backend.settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def process_file(file: pathlib.Path):
    import backend.tagging
    import backend.tagging.perframe

    logging.info(f"processing {str(file)}")

    processors: list[backend.tagging.IVideoProcessor] = [
        backend.tagging.VideoTaggerRunner(
            taggers=[
                lambda: backend.tagging.perframe.VideoPerFrameTagger(
                    "tf-efficientnet",
                ),
                lambda: backend.tagging.VideoMetadataTagger(),
            ]
        ),
        backend.tagging.VideoThumbnailer(),
        backend.tagging.VideoHasher(),
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


def index_files(files: list[pathlib.Path]):
    """Index files. Expects that there are no existing records for them."""

    @utils.time_exec
    def process_all_files():
        if settings.concurrent_videos == 1:
            return list(map(process_file, files))
        else:
            with concurrent.futures.ProcessPoolExecutor(
                settings.concurrent_videos
            ) as p:
                return list(p.map(process_file, files))

    took, _ = process_all_files()

    return took


def index_new_files(directories: list[str], extensions: list[str]):
    """Indexes new files.

    Not meant to be called directly (but through a task!)
    """

    # currently, this appears rather slow as we check whether each file is in
    # database one by one
    def is_new_file(file: pathlib.Path):
        return backend.models.Videos.get_by_filename(str(file.absolute())) is None

    files = list(find_video_files(directories, extensions))
    logging.info(f"Found {len(files)} multimedia files.")
    new_files = list(filter(is_new_file, files))
    logging.info(f"Found {len(new_files)} new multimedia files.")

    if len(new_files) > 0:
        took = index_files(new_files)
        files_count = len(new_files)
        logging.info(f"Indexing {files_count} files took {(took)/(10**9)}s.")
    else:
        logging.info("No new files were indexed.")


def reindex_all(directories: list[str], extensions: list[str]):
    """Deletes the index and then reindexes all files.

    Not meant to be called directly (but through a task!)
    """
    backend.models.Videos.delete_all()
    files = list(find_video_files(directories, extensions))

    took = index_files(files)

    files_count = len(files)
    logging.info(f"Indexing {files_count} files took {(took)/(10**9)}s.")


class VideoIndexer:
    def __init__(self, video_processors: list[backend.tagging.IVideoProcessor]):
        self.processors = video_processors

    def index_video(self, path: pathlib.Path):
        # TODO: only update old/missing if not exists
        video = Video(filenames=[str(path)], filehash="", tags=[])
        for processor in self.processors:
            try:
                # TODO: only necessary if missing/old (in which case I should)
                # remove old data first
                video = processor.process(video, path)
            except Exception as e:
                logging.exception(e)
        from pymongo.errors import DuplicateKeyError

        try:
            backend.models.Videos.insert_one(video.dict())
        except DuplicateKeyError as e:
            logging.exception(e)
            logging.warning(f"Could not insert {path} as it it already exists.")
