import abc
import pathlib
import typing

from backend.classifiers.prediction import Video, VideoTag


class IVideoProcessor(metaclass=abc.ABCMeta):
    """IVideoProcessors"""

    @abc.abstractmethod
    def process(self, video: Video, video_path: pathlib.Path) -> Video:
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

    def process(self, video: Video, video_path: pathlib.Path) -> Video:
        self._initialize()
        for tagger in self._taggers_instances:
            video.tags += tagger.tag(video_path)
        return video


class VideoThumbnailer(IVideoProcessor):
    """Creates and uploads thumbnails for a video"""

    def process(self, video: Video, video_path: pathlib.Path) -> Video:
        from backend.tasks.default import rpc_create_video_thumbnails

        # keys = rpc_create_video_thumbnails.send(video_path).get_result(
        # block=True, timeout=60 * 60 * 1_000
        # )
        keys = rpc_create_video_thumbnails(video_path)
        video.thumbnails = keys
        return video


class VideoHasher(IVideoProcessor):
    """Add file hash to a video"""

    def process(self, video: Video, video_path: pathlib.Path) -> Video:
        from backend.filehash import file_hash

        filehash = file_hash(str(video_path))
        video.filehash = filehash
        return video


class VideoMetadataTagger(IVideoTagger):
    """Extracts metadata from the video file and adds tags"""

    def tag(self, video_path: pathlib.Path) -> list[VideoTag]:
        import av

        with av.open(str(video_path)) as container:
            stream = container.streams.video[0]
            ctx = stream.codec_context
            width = ctx.width
            height = ctx.height
            codec_name = ctx.name
        extension = (
            video_path.suffix[1:] if video_path.suffix[0] == "." else video_path.suffix
        )

        tags = [
            VideoTag(model="metadata", tag=f"width:{width}", conf=1.0),
            VideoTag(model="metadata", tag=f"height:{height}", conf=1.0),
            VideoTag(model="metadata", tag=f"video_codec:{codec_name}", conf=1.0),
            VideoTag(model="metadata", tag=f"extension:{extension}", conf=1.0),
        ]

        return tags
