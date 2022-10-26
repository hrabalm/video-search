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


class BeitClassifier(AbstractClassifier):
    import timeit

    from transformers import BeitFeatureExtractor, BeitForImageClassification

    def __init__(self, model_name="google/vit-base-patch16-224"):
        self._model_name = model_name
        self._feature_extractor = self.BeitFeatureExtractor.from_pretrained(
            "microsoft/beit-base-patch16-224-pt22k-ft22k"
        )
        self._model = self.BeitForImageClassification.from_pretrained(
            "microsoft/beit-base-patch16-224-pt22k-ft22k"
        )

    def classify_batch(self, batch: Collection) -> list:
        start = self.timeit.default_timer()

        inputs = self._feature_extractor(batch, return_tensors="pt")
        outputs = self._model(**inputs)  # type: ignore
        logits = outputs.logits
        predicted_classes_indices = logits.argmax(-1).label
        predicted_classes_labels = map(
            lambda x: self._model.config.id2label[x], predicted_classes_indices
        )
        predicted_classes_scores = logits.argmax(-1).score

        decoded_predictions = list(
            [{"score": score, "label": label}]
            for score, label in zip(predicted_classes_scores, predicted_classes_labels)
        )
        end = self.timeit.default_timer()
        took = end - start
        print(f"Batch of {len(batch)} done in {took}s. {len(batch)/took} frames / s.")

        top1_predictions = map(
            lambda preds: sorted(preds, key=lambda p: p["score"], reverse=True)[0],
            decoded_predictions,
        )
        results = map(
            lambda x: PerFramePrediction(score=x["score"], label=x["label"]),
            top1_predictions,
        )

        return list(results)


def recover_frames(filename, predictions: Collection[PerFramePrediction]):
    wanted_pts = set()
    frames_by_pts = {}

    for pred in predictions:
        if pred.pts is not None:
            wanted_pts.add(pred.pts)
        else:
            raise Exception("Cannot recover frame when pts is not known.")

    for frame in read_frames(filename):
        if frame.pts in wanted_pts:
            frames_by_pts[frame.pts] = frame.to_image()

    return [frames_by_pts[pred.pts] for pred in predictions]


def annote_and_save(filename, classifier, output_filename, min_conf=0.5):
    if pathlib.Path(output_filename).is_file():
        print(
            f"Skipping {classifier.__class__.__name__} because {output_filename} already exists."
        )
        return

    grouped = tag_video_file(filename, classifier, keyframes_only=True)

    filtered_grouped = filter(lambda x: x.best_score() >= min_conf, grouped)

    best_predictions = [
        (g.best(), g.count())
        for g in sorted(filtered_grouped, reverse=True, key=lambda x: x.best_score())
    ]
    best_predictions_images = recover_frames(
        filename, list(map(lambda x: x[0], best_predictions))
    )
    best_predictions_images_annoted = list(
        starmap(
            lambda pred, img: annote_image(
                img, f"{pred[0].label}={pred[0].score}, count={pred[1]}"
            ),
            zip(best_predictions, best_predictions_images),
        )
    )

    with open(output_filename, "wb") as f:
        save_images_to_zipfile(best_predictions_images_annoted, f)


def manual():
    classifier = EfficientNetClassifierLarge()
    # classifier = VitClassifier()
    grouped = tag_video_file(BBB_FILENAME, classifier, keyframes_only=True)

    # grouped_by_count = sorted(grouped, key=lambda g: g.count(), reverse=True)
    # for g in grouped_by_count:
    #     print(g)
    #     print()

    # print(grouped)

    # grouped_filtered = list(filter(
    #     lambda g: g.best_score() > 0.95,
    #     grouped
    # ))

    # print(grouped_filtered)
    best_predictions = [
        (g.best(), g.count())
        for g in sorted(grouped, reverse=True, key=lambda x: x.best_score())
    ]
    best_predictions_images = recover_frames(
        BBB_FILENAME, list(map(lambda x: x[0], best_predictions))
    )
    best_predictions_images_annoted = list(
        starmap(
            lambda pred, img: annote_image(
                img, f"{pred[0].label}={pred[0].score}, count={pred[1]}"
            ),
            zip(best_predictions, best_predictions_images),
        )
    )

    with open("best_predictions.enetl+c.cbz", "wb") as f:
        save_images_to_zipfile(best_predictions_images_annoted, f)


def main():
    annote_and_save(
        BBB_FILENAME,
        HuggingFaceImageClassifier("microsoft/beit-base-patch16-224-pt22k-ft22k"),
        "bbb-beit-base-patch16-224-pt22k-ft22k.cbz",
    )

    # annote_and_save(
    #     TRANSFORMERS_FILENAME,
    #     HuggingFaceImageClassifier("microsoft/beit-base-patch16-224-pt22k-ft22k"),
    #     "trn-beit-base-patch16-224-pt22k-ft22k.cbz",
    # )


if __name__ == "__main__":
    main()
