from typing import Callable, NamedTuple


def make_efficientnet():
    import backend.classifiers.efficientnet

    return backend.classifiers.efficientnet.EfficientNetClassifier()


class ClassifiersRecord(NamedTuple):
    make_func: Callable
    input_resolution: tuple[int, int]


classifiers_catalog = {
    "tf-efficientnet": ClassifiersRecord(make_efficientnet, (224, 224)),
}
