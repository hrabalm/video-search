import gridfs
import pymongo

from backend.classifiers.prediction import codec_options
from backend.settings import settings

_mongo_client = pymongo.MongoClient(
    host=settings.mongo_host,
    port=settings.mongo_port,
    username=settings.mongo_username,
    password=settings.mongo_password,
)
db = _mongo_client[settings.mongo_db]
db_videos = db.get_collection("videos", codec_options=codec_options)
fs = gridfs.GridFS(db)
