import pickle
from functools import reduce
from itertools import starmap
from typing import Collection, Tuple

import numpy as np

RawResult = tuple[str, str, np.float16]
RawResults = Collection[RawResult]

with open("raw_results_large.pickle", "rb") as f:
    raw_results = pickle.load(f)

from collections import defaultdict

unique_tags = set()
histogram = defaultdict(lambda: 0)
max_conf = defaultdict(lambda: 0.0)
occurences = defaultdict(lambda: [])

for i, tag in enumerate(raw_results):
    _, name, conf = tag[0]
    unique_tags.add(name)
    histogram[name] += 1
    max_conf[name] = max(max_conf[name], conf)
    occurences[name].append((conf, i))

results = [
    (max_conf[name], histogram[name], name, max(occurences[name]))
    for name in unique_tags
]
results.sort(reverse=True)

filtered_results = list(filter(lambda x: x[0] > 0.5, results))
# for res in filtered_results:
# print(res)
print(*filtered_results, sep="\n")

# additional raw data processing:
# moving average over a few adjacent frames
def combine_results(raw_results):
    tags_by_name = [(res[0][1], res[0]) for res in raw_results]

    def f(accumulator, new_record):
        if len(accumulator) == 0:
            accumulator.append((new_record[0], [new_record[1]]))
        elif accumulator[-1][0] == new_record[0]:
            accumulator[-1][1].append(new_record[1])
        else:
            accumulator.append((new_record[0], [new_record[1]]))
        return accumulator

    return reduce(f, tags_by_name, [])


combined_results = combine_results(raw_results)

from toolz import nth

from indexing import read_frames, read_frames_resized


def get_frame(filename, frame_idx):
    # note: probably very slow
    frames = read_frames(filename)
    return nth(frame_idx, frames)


def get_frames(filename, frame_indices: Collection[int]):
    # Unlinke get_frame above, this only needs a single pass through the video
    # file
    frame_idxs_set = set(frame_indices)
    frame_storage = {}
    frames = read_frames(filename)
    for i, frame in enumerate(frames):
        if i in frame_idxs_set:
            frame_storage[i] = frame.to_image()
    return list(map(lambda idx: frame_storage[idx], frame_indices))


import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


def annote_image(image, text: str):
    import PIL.Image
    import PIL.ImageDraw
    import PIL.ImageFont

    try:
        font = PIL.ImageFont.truetype("DejaVuSans.ttf", 32)
    except:
        font = PIL.ImageFont.load_default()
    draw = PIL.ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font, fill=(225, 0, 0))
    return image


def result_frame(filename, result):
    conf, count, image_class, best_occurance = result
    _, frame_idx = best_occurance
    try:
        font = PIL.ImageFont.truetype("DejaVuSans.ttf", 32)
    except:
        font = PIL.ImageFont.load_default()
    image = get_frame(filename, frame_idx).to_image().resize((512, 512))
    draw = PIL.ImageDraw.Draw(image)
    draw.text((10, 10), f"{image_class}: {conf}", font=font, fill=(225, 0, 0))
    return image


def best_result_frames(filename, results):
    frame_confidences = [res[3][0] for res in results]
    frame_classes = [res[2] for res in results]
    frame_indices = [res[3][1] for res in results]
    frames = get_frames(filename, frame_indices)
    annoted_frames = list(
        starmap(
            lambda image, image_class, confidence: annote_image(
                image, f"{image_class}: {confidence}"
            ),
            zip(frames, frame_classes, frame_confidences),
        )
    )
    return annoted_frames


# for res in filtered_results:
#     FILENAME = "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4"
#     print(res)
#     _, frame_idx = res[3]
#     frame = get_frame(FILENAME, frame_idx)
#     image = frame.to_image()
#     print(image)
#     image.show()
#     input("Ent")

FILENAME = "/home/mhn/videos/bbb_sunflower_1080p_30fps_normal.mp4"
# annoted_best = [result_frame(FILENAME, res) for res in filtered_results]
annoted_best = best_result_frames(FILENAME, filtered_results)
with open("annoted_best_large.pickle", "wb") as f:
    pickle.dump(annoted_best, f)
