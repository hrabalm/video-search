import threading

import dramatiq
import numpy as np
import tensorflow as tf
from toolz import compose_left

from classifiers.abstractclassifier import AbstractClassifier
from classifiers.prediction import PerFramePrediction

# If there is a GPU available, enable memory_growth
physical_devices = tf.config.list_physical_devices("GPU")
if len(physical_devices):
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Thread-local data
local = threading.local()


def to_prediction(decoded_prediction: list[tuple]) -> PerFramePrediction:
    """Converts from tensorflow prediction output to our `Prediction
    representation.
    `"""
    return PerFramePrediction(
        score=decoded_prediction[0][2], label=decoded_prediction[0][1]
    )


class EfficientNetClassifier(AbstractClassifier):
    def __init__(self):
        self._model = tf.keras.applications.EfficientNetV2B0(weights="imagenet")

    def classify_batch(self, batch) -> list:
        preprocessed_images = map(
            compose_left(
                lambda img: np.asarray(img),
                lambda img: tf.keras.applications.efficientnet_v2.preprocess_input(img),
                lambda img: tf.convert_to_tensor(img),
            ),
            batch,
        )
        predictions = self._model.predict(preprocessed_images)
        decoded_predictions = tf.keras.applications.efficientnet_v2.decode_predictions(
            predictions, top=1
        )
        results = map(to_prediction, decoded_predictions)
        return list(results)

    @property
    def required_resolution(self) -> tuple[int, int]:
        return (224, 224)


class EfficientNetClassifierLarge(AbstractClassifier):
    def __init__(self):
        self._model = tf.keras.applications.EfficientNetV2B3(weights="imagenet")

    def classify_batch(self, batch) -> list:
        preprocessed_images = map(
            compose_left(
                lambda img: np.asarray(img),
                lambda img: tf.keras.applications.efficientnet_v2.preprocess_input(img),
                lambda img: tf.convert_to_tensor(img),
            ),
            batch,
        )
        predictions = self._model.predict(preprocessed_images)
        decoded_predictions = tf.keras.applications.efficientnet_v2.decode_predictions(
            predictions, top=1
        )
        results = map(to_prediction, decoded_predictions)
        return list(results)

    @property
    def required_resolution(self) -> tuple[int, int]:
        return (224, 224)


def get_classifier(classifier_type: type):
    """Get thread-local instance of the given classifier."""
    name = classifier_type.__name__
    classifier = getattr(local, name, None)
    if classifier is None:
        classifier = classifier_type()
        setattr(local, name, classifier)
    return classifier


@dramatiq.actor
def classify_batch(batch):
    classifier: AbstractClassifier = get_classifier(EfficientNetClassifier)
    return classifier.classify_batch(batch)
