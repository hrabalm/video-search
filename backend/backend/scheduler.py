from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from backend.settings import settings

jobstores = {
    "default": MongoDBJobStore(
        host=settings.mongo_host,
        port=settings.mongo_port,
        username=settings.mongo_username,
        password=settings.mongo_password,
    ),
}

executors = {"default": ProcessPoolExecutor(4)}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
