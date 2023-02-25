import abc
import pathlib
import typing

from backend.classifiers.prediction import Video, VideoTag


class IVideoProcessor(metaclass=abc.ABCMeta):
    """IVideoProcessors"""

    @abc.abstractmethod
    def process(self, video, video_path: pathlib.Path) -> Video:
        raise NotImplementedError


class IVideoTagger(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def tag(self, video_path: pathlib.Path) -> list[VideoTag]:
        raise NotImplementedError


class VideoTaggerRunner(IVideoProcessor):
    """Runs IVideoTagger taggers and adds the resulting tags to the video.

    tagger: list of functions that create taggers, so that they are created
            this is done so that they are created lazily
    """

    def __init__(self, taggers: list[typing.Callable[[], IVideoTagger]]):
        self._tagger_makers = taggers
        self._taggers_instances: list = []
        self._is_initialized = False

    def _initialize(self):
        if not self._is_initialized:
            self._taggers_instances = [
                make_tagger() for make_tagger in self._tagger_makers
            ]
            self._is_initialized = True

    def process(self, video, video_path: pathlib.Path) -> Video:
        self._initialize()
        for tagger in self._taggers_instances:
            video.tags += tagger.tag(video_path)
        return video


class VideoThumbnailer(IVideoProcessor):
    """Creates and uploads thumbnails for a video"""

    pass  # TODO


class VideoHasher(IVideoProcessor):
    """Add file hash to a video"""

    pass  # TODO


class VideoMetadataTagger(IVideoTagger):
    """Extracts metadata from the video file and adds tags"""
