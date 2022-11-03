import pymongo

from settings import settings

_mongo_client = pymongo.MongoClient(
    host=settings.mongo_host,
    port=settings.mongo_port,
    username=settings.mongo_username,
    password=settings.mongo_password,
)
db = _mongo_client[settings.mongo_db]
