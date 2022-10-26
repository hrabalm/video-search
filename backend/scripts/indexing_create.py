import pickle

from classifiers.vit import VitClassifier
from indexing import tag_video_file

if __name__ == "__main__":
    raw_results = tag_video_file(
        "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4",
        VitClassifier(),
        4000,
    )

    with open("vit.torch.pickle", "wb") as f:
        pickle.dump(raw_results, f)
