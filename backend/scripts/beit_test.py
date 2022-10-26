import pathlib
from itertools import starmap
from typing import Collection

from classifiers.abstractclassifier import AbstractClassifier
from classifiers.efficientnet import EfficientNetClassifier, EfficientNetClassifierLarge
from classifiers.prediction import PerFramePrediction
from classifiers.vit import HuggingFaceImageClassifier, VitClassifier
from indexing import (
    annote_image,
    group_predictions,
    read_frames,
    select_tags,
    tag_video_file,
)
from scripts.cbz import save_images_to_zipfile

BBB_FILENAME = "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4"
TRANSFORMERS_FILENAME = "/home/mhn/videos/transf.mp4"

if __name__ == "__main__":
    classifier = HuggingFaceImageClassifier(
        "microsoft/beit-base-patch16-224-pt22k-ft22k"
    )
    keys = sorted(classifier._model.model.config.id2label.keys())
    print(keys[0], keys[-1])
    for i in range(keys[0], keys[-1] + 1):
        if i not in keys:
            print("notfound", i)
    print(classifier._model.model.config)
