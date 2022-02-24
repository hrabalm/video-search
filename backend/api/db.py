import os

import pymongo

_DB_HOST = os.getenv("SQL_HOST")
_DB_PORT = os.getenv("SQL_PORT")
_DB_NAME = os.getenv("SQL_DB")
_DB_USER = os.getenv("SQL_USER")
_DB_PASSWORD = os.getenv("SQL_PASSWORD")

_mongo_client = pymongo.MongoClient(_DB_HOST, int(_DB_PORT) if _DB_PORT else None)
db = _mongo_client[_DB_NAME if _DB_NAME else "default"]
