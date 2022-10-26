from toolz import count

from classifiers.efficientnet import EfficientNetClassifier
from classifiers.vit import (
    HuggingFaceImageClassifier,
    VitClassifier,
    VitClassifierLarge,
)
from indexing import read_frames, select_tags, tag_video_file

FILENAME = "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4"
# FILENAME = "/home/mhn/videos/[2007]-Transformers-[EN].mp4"


def main():
    # classifier = VitClassifier()
    # classifier = HuggingFaceImageClassifier("nvidia/mit-b2")
    classifier = EfficientNetClassifier()
    raw = tag_video_file(FILENAME, classifier, keyframes_only=True)
    selected = select_tags(raw, 0.5)
    only = set([tag.label for tag in selected])
    print(only)


if __name__ == "__main__":
    main()
