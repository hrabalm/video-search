import pickle
import timeit

from toolz import take

from classifiers.efficientnet import EfficientNetClassifierLarge
from classifiers.vit import VitClassifier
from indexing import read_frames, read_frames_resized, tag_video_file

FILENAME = "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4"

if __name__ == "__main__":
    # SIZE = 1000

    # classifier = VitClassifier()
    # with open(FILENAME, "rb") as file:
    #     frames = read_frames_resized(file, (224, 224))
    #     sample = list(take(SIZE, frames))

    # start = timeit.default_timer()
    # classifier.classify_batch(sample)
    # end = timeit.default_timer()
    # print(f"VIT took {end-start}s.")

    # enet = EfficientNetClassifierLarge()
    # with open(FILENAME, "rb") as file:
    #     frames = read_frames_resized(file, (224, 224))
    #     sample = list(take(SIZE, frames))

    # start = timeit.default_timer()
    # enet.classify_batch(sample)
    # end = timeit.default_timer()
    # print(f"Enet took {end-start}s.")

    # classifier = VitClassifier()
    # with open(FILENAME, "rb") as file:
    #     frames = read_frames_resized(file, (224, 224))
    #     sample = list(take(SIZE, frames))

    # start = timeit.default_timer()
    # classifier.classify_batch(sample)
    # end = timeit.default_timer()
    # print(f"VIT took {end-start}s.")

    # with open("vit.pickle", "wb") as f:
    #     pickle.dump(raw_results, f)
    from toolz import count

    print(count(read_frames(FILENAME)))
