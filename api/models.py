from db import db
from bson import json_util
import json


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


Videos.add(
    {
        "name": "Nemesis",
        "tags": [
            "cat",
            "dog",
            {"tag": "cat", "type": "nn"},
            {"tag": "dog", "type": "nn"},
            {"tag": "cat", "type": "nn"},
        ],
    }
)
