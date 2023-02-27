import pymongo
from bson.objectid import ObjectId

from backend.api.db import db_videos


class TagImages:
    pass


class Files:
    pass


class Tags:
    @staticmethod
    def get_all():
        tags = list(db_videos.distinct("tags.tag"))
        return tags


class Videos:
    @staticmethod
    def _put_images(video):
        pass

    @staticmethod
    def _get_images(video):
        pass

    @staticmethod
    def insert_one(video):
        db_videos.insert_one(video)
        print("Inserted")

    @staticmethod
    def get(id: str):
        return db_videos.find_one({"_id": ObjectId(id)})

    @staticmethod
    def get_by_filename(filename: str):
        return db_videos.find_one({"filenames": filename})

    @staticmethod
    def get_all():
        return list(
            db_videos.find().sort("filenames", pymongo.ASCENDING)
        )  # FIXME: check

    @staticmethod
    def get_by_tags(tags: list[str], min_conf: float):
        if len(tags) > 0:
            return list(
                db_videos.find(
                    {
                        "$and": [
                            {
                                "tags": {
                                    "$elemMatch": {
                                        "conf": {"$gt": min_conf},
                                        "tag": tag,
                                    }
                                }
                            }
                            for tag in tags
                        ]
                    }
                ).sort("filenames", pymongo.ASCENDING)
            )  # FIXME: check
        return Videos.get_all()
