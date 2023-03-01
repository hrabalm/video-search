import logging

import pymongo
from bson.objectid import ObjectId

from backend.api.db import db_status, db_videos
from backend.settings import settings

db_videos.create_index("filenames.0", unique=True, background=True)
db_videos.create_index("tags.tag", background=True)


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
    def get_all_with_pagination_range(count_per_page: int, last_filename: str):
        return list(
            db_videos.find(
                {
                    "filenames.0": {
                        "$gt": last_filename,
                    }
                }
            )
            .sort("filenames.0", pymongo.ASCENDING)
            .limit(count_per_page)
        )

    @staticmethod
    def get_all_with_pagination(items_per_page: int, page_number: int):
        return list(
            db_videos.find({})
            .sort("filenames.0", pymongo.ASCENDING)
            .skip((page_number - 1) * items_per_page)
            .limit(items_per_page)
        )

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
    def get_by_tags_with_pagination(
        tags: list[str], min_conf: float, items_per_page: int, page_number: int
    ):
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
                )
                .sort("filenames.0", pymongo.ASCENDING)
                .skip((page_number - 1) * items_per_page)
                .limit(items_per_page)
            )
        return Videos.get_all_with_pagination(items_per_page, page_number)

    @staticmethod
    def get_by_tags_with_pagination_range(
        tags: list[str], min_conf: float, count_per_page: int, last_filename: str = ""
    ):
        if len(tags) > 0:
            return list(
                db_videos.find(
                    {
                        "$and": (
                            [
                                {
                                    "filenames.0": {
                                        "$gt": last_filename,
                                    }
                                },
                            ]
                            + [
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
                        )
                    }
                )
                .sort("filenames.0", pymongo.ASCENDING)
                .limit(count_per_page)
            )
        return Videos.get_all_with_pagination_range(count_per_page, last_filename)

    @staticmethod
    def count(
        tags: list[str] = [], min_conf: float = settings.minimum_confidence_shown
    ):
        if len(tags) > 0:
            return db_videos.count_documents(
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
            )
        return db_videos.count_documents({})

    @staticmethod
    def delete_all():
        db_videos.delete_many({})


class Status:
    @staticmethod
    def set(key, old_value: dict | None, new_value: dict) -> bool:
        db_status.create_index("key", unique=True)
        if not old_value:
            old_value = {"key": key}
        try:
            db_status.find_one_and_replace(old_value, new_value, upsert=True)
            return True
        except Exception as e:
            logging.warning(e)
        return False

    @staticmethod
    def get(key: str) -> dict | None:
        return db_status.find_one({"key": key})
