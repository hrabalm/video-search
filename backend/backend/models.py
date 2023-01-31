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
    def get_all():
        return list(db_videos.find())

    @staticmethod
    def get_by_tags(tags: list[str], min_conf: float):
        return db_videos.find(
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
