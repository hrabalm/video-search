import json

from bson import json_util

from api.db import db


def to_json(x):
    json.loads(json_util.dumps(x))


class Tags:
    @staticmethod
    def get_all():
        tags = list(db.videos.distinct("tags"))
        return {"tags": tags}


class Videos:
    @staticmethod
    def add(video):
        db.videos.insert_one(video)

    @staticmethod
    def get_all():
        videos = db.videos.find()
        other = to_json(videos)
        return {"vidoes": str(db.videos.find()), "other": other}
