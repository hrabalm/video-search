from classifiers.vit import VitClassifier, VitClassifierLarge
from indexing import count_keyframes, read_frames, select_tags, tag_video_file

FILENAME = "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4"
FILENAME = "/home/mhn/videos/[2007]-Transformers-[EN].mp4"


def main():
    print(count_keyframes(FILENAME))


if __name__ == "__main__":
    main()
