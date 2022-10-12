import abc

import classifiers.prediction


class AbstractClassifier(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    def classify(self, image) -> classifiers.prediction.Prediction:
        return self.classify_batch([image])[0]

    @abc.abstractmethod
    def classify_batch(self, batch) -> list[classifiers.prediction.Prediction]:
        raise NotImplementedError
