import glob
import logging
import multiprocessing
import pathlib
from typing import Collection

import models
from settings import settings
from toolz import concat
from utils import get_project_root

import indexing
from api.db import db
from classifiers.efficientnet import EfficientNetClassifier
from classifiers.prediction import Video, VideoTag, codec_options


def is_multimedia_file(file: pathlib.Path, extensions: set[str]):
    if file.is_file() and str.lower(file.suffix) in extensions:
        return True
    else:
        return False


def is_new(file: pathlib.Path):
    # TODO
    return True


def index_video_file(f: pathlib.Path):
    assert f.is_file()

    logging.info(f"Processing {f}...")
    tags = indexing.tag_video(str(f), EfficientNetClassifier())
    # print(result)
    # for r in tags:
    # print("a", r)
    # print("b", r.dict())
    # print("c", VideoTag(**r.dict()))

    processed_tags = []

    # collection.insert_one(r.dict())

    video = Video(filenames=[f.name], filehash="TODO", tags=list(tags))
    # collection.insert_one(video.dict())
    models.Videos.insert_one(video.dict())
    print(f"Inserting {video.dict()}")


collection = db.get_collection("collection", codec_options=codec_options)


def save_video_record(video_record, video_records=collection):
    # TODO: upload images to gridfs to make document itself smaller
    collection.insert_one(video_record.dict())


def get_multimedia_files(directories: Collection[pathlib.Path]):
    files = list(concat(d.glob("**/*") for d in directories))
    multimedia_files = list(
        filter(lambda x: is_multimedia_file(x, settings.video_extensions), files)
    )
    new_files = list(filter(is_new, multimedia_files))
    return new_files


def index_files(multimedia_files: list[pathlib.Path]):
    with multiprocessing.Pool(1) as pool:
        pool.map(
            index_video_file,
            multimedia_files,
        )


def clear_collection():
    pass


DIRECTORIES = {get_project_root() / ".test_data"}
MULTIMEDIA_FILES = get_multimedia_files(DIRECTORIES)


print(MULTIMEDIA_FILES)

TEST_FILE = MULTIMEDIA_FILES[0]

index_video_file(TEST_FILE)

print(list(collection.find()))
