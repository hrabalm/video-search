from db import db

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
        return db.videos.find()