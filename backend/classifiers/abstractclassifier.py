import abc

import classifiers.prediction


class AbstractClassifier(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    def classify(self, image) -> list[classifiers.prediction.PerFramePrediction]:
        return self.classify_batch([image])[0]

    @abc.abstractmethod
    def classify_batch(
        self, batch
    ) -> list[list[classifiers.prediction.PerFramePrediction]]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def required_resolution(self) -> tuple[int, int]:
        raise NotImplementedError
