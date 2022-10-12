import timeit
from typing import Collection

import transformers

from classifiers.abstractclassifier import AbstractClassifier
from classifiers.prediction import Prediction


class VitClassifier(AbstractClassifier):
    def __init__(self):
        self._model = transformers.pipeline(
            "image-classification",
            framework="pt",
        )

    def classify_batch(self, batch: Collection) -> list:
        start = timeit.default_timer()
        decoded_predictions = list(self._model(batch))
        end = timeit.default_timer()
        took = end - start
        print(f"Batch of {len(batch)} done in {took}s. {len(batch)/took} frames / s.")

        top1_predictions = map(
            lambda preds: sorted(preds, key=lambda p: p["score"], reverse=True)[0],
            decoded_predictions,
        )
        results = map(
            lambda x: Prediction(score=x["score"], label=x["label"]), top1_predictions
        )

        return list(results)


class VitClassifierLarge(AbstractClassifier):
    def __init__(self):
        self._model = transformers.pipeline(
            "image-classification",
            model="google/vit-large-patch16-224",
            framework="pt",
        )

    def classify_batch(self, batch: Collection) -> list:
        start = timeit.default_timer()
        decoded_predictions = list(self._model(batch))
        end = timeit.default_timer()
        took = end - start
        print(f"Batch of {len(batch)} done in {took}s. {len(batch)/took} frames / s.")

        top1_predictions = map(
            lambda preds: sorted(preds, key=lambda p: p["score"], reverse=True)[0],
            decoded_predictions,
        )
        results = map(
            lambda x: Prediction(score=x["score"], label=x["label"]), top1_predictions
        )

        return list(results)


class HuggingFaceImageClassifier(AbstractClassifier):
    def __init__(self, model_name="google/vit-base-patch16-224"):
        self._model_name = model_name
        self._model = transformers.pipeline(
            "image-classification",
            model=model_name,
            framework="pt",
        )

    def classify_batch(self, batch: Collection) -> list:
        start = timeit.default_timer()
        decoded_predictions = list(self._model(batch))
        end = timeit.default_timer()
        took = end - start
        print(f"Batch of {len(batch)} done in {took}s. {len(batch)/took} frames / s.")

        top1_predictions = map(
            lambda preds: sorted(preds, key=lambda p: p["score"], reverse=True)[0],
            decoded_predictions,
        )
        results = map(
            lambda x: Prediction(score=x["score"], label=x["label"]), top1_predictions
        )

        return list(results)
