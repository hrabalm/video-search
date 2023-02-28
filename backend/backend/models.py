import pymongo
from bson.objectid import ObjectId

from backend.api.db import db_videos
from backend.settings import settings


class TagImages:
    pass


class Files:
    pass


class Tags:
    @staticmethod
    def get_all():
        return sorted(list(set(t["tag"] for t in TagsV2.get_all())))


class TagsV2:
    @staticmethod
    def get_all():
        tags = db_videos.aggregate(
            [
                {"$unwind": "$tags"},
                {"$match": {"tags.conf": {"$gte": settings.minimum_confidence_shown}}},
                {
                    "$project": {
                        "_id": 0,
                        "tag": "$tags.tag",
                        "conf": "$tags.conf",
                        "model": "$tags.model",
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "tag": "$tag",
                            "model": "$model",
                        },
                        "conf": {"$max": "$conf"},
                        "count": {"$count": {}},
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "tag": "$_id.tag",
                        "model": "$_id.model",
                        "conf": "$conf",
                        "count": "$count",
                    }
                },
            ]
        )
        return list(tags)


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
        return list(db_videos.find().sort("filenames.0", pymongo.ASCENDING))

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
                ).sort("filenames.0", pymongo.ASCENDING)
            )
        return Videos.get_all()

    @staticmethod
    def delete_all():
        db_videos.delete_many({})
