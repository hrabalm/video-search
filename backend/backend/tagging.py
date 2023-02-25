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

ENABLE_MODEL_CACHE = False
models_cache = {}

def get_model(name, make_model: typing.Callable):
    if ENABLE_MODEL_CACHE:
        if name in models_cache:
            return models_cache[name]
        model = make_model()
        models_cache[name] = model
        return model
    else:
        return make_model()

class VideoPerFrameTagger(IVideoTagger):
    """Passes video keyframes through a image classification model and returns
    the results as tags."""

    def __init__(
        self, model_name: str, model_maker: typing.Callable
    ):
        self.model_name = model_name
        self._model_maker = model_maker
        self._model = None

    def _ensure_initialized(self):
        if not self._model:
            # self._model = self._model_maker()
            self._model = get_model(self.model_name, self._model_maker)

    def tag(self, video_path: pathlib.Path) -> list[VideoTag]:
        import backend.indexing

        assert video_path.is_file()
        self._ensure_initialized()
        tags = backend.indexing.tag_video(str(video_path), self._model)
        return list(tags)


class TestTagger(IVideoTagger):
    def tag(self, video_path: pathlib.Path) -> list[VideoTag]:
        import backend.indexing
        from backend.classifiers.efficientnet import EfficientNetClassifier

        assert video_path.is_file()
        tags = backend.indexing.tag_video(str(video_path), EfficientNetClassifier())

        return list(tags)


class VideoMetadataTagger(IVideoTagger):
    """Extracts metadata from the video file and adds tags"""
