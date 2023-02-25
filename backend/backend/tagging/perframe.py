import pathlib
import typing

import backend.tagging
from backend.classifiers.prediction import VideoTag

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


class VideoPerFrameTagger(backend.tagging.IVideoTagger):
    """Passes video keyframes through a image classification model and returns
    the results as tags."""

    def __init__(self, model_name: str, model_maker: typing.Callable):
        self.model_name = model_name
        self._model_maker = model_maker
        self._model = None

    def _ensure_initialized(self):
        if not self._model:
            self._model = get_model(self.model_name, self._model_maker)

    def tag(self, video_path: pathlib.Path) -> list[VideoTag]:
        import backend.indexing

        assert video_path.is_file()
        self._ensure_initialized()
        tags = backend.indexing.tag_video(str(video_path), self._model)
        return list(tags)

