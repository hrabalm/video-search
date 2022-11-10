from api.db import db_videos


class TagImages:
    pass


class Files:
    pass


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
        return db_videos.find()
