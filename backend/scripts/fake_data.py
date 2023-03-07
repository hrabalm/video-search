import random
import uuid

from backend.classifiers.prediction import Video, VideoTag
from backend.models import Videos

random.seed(42)

UNIQUE_TAGS_COUNT = 5000
TAGS_PER_VIDEO = 10
VIDEOS_COUNT = 10000

TAGS = [f"z_fictionaltag_{i}" for i in range(UNIQUE_TAGS_COUNT)]


def create_video(tags):
    filename = f"/z/fake/{uuid.uuid4()}.mkv"
    tags = [
        VideoTag(
            model="z_fictionaltagger",
            tag=tag,
            frame_pts=[],
            conf=random.uniform(0.5, 1.0),
        )
        for tag in tags
    ]

    video = Video(filenames=[filename], filehash="", tags=tags)

    Videos.insert_one(video.dict())


for _ in range(VIDEOS_COUNT):
    tags = random.sample(TAGS, k=TAGS_PER_VIDEO)
    create_video(tags)
