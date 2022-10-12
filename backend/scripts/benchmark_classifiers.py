import time

import click

from classifiers.efficientnet import EfficientNetClassifier, EfficientNetClassifierLarge
from classifiers.vit import VitClassifier, VitClassifierLarge
from indexing import count_keyframes, tag_video_file

factories = [
    lambda: EfficientNetClassifier(),
    lambda: EfficientNetClassifierLarge(),
    lambda: VitClassifier(),
    lambda: VitClassifierLarge(),
]


@click.command()
@click.argument("filename")
def benchmark(filename):
    count = count_keyframes(filename)
    results_times = []
    results = []

    for classifier_factory in factories:
        classifier = classifier_factory()

        start = time.perf_counter_ns()
        tags = tag_video_file(filename, classifier, keyframes_only=True)
        end = time.perf_counter_ns()

        took_ns = end - start

        results_times.append((classifier.__class__.__name__, took_ns))
        results.append(tags)

    print(count)
    print(results_times)


if __name__ == "__main__":
    benchmark()
