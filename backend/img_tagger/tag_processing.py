from collections import defaultdict
from typing import List

from shared import ImageTag, VideoTag


def determine_video_tag(images: List[ImageTag]) -> VideoTag:
    tags = defaultdict(lambda: 0.0)
    sources = {}

    for image_tag in images:
        for partial_tag in image_tag.tags:
            tags[partial_tag.name] += partial_tag.conf
            sources[partial_tag.source] = True

    for tag, weight in tags.items():
        print(tag, weight)

    # FIXME
    return VideoTag()
