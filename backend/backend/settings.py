from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # MongoDB
    mongo_host = ["mongo"]
    mongo_port = 27017
    mongo_db = "default"
    mongo_username: Optional[str] = None
    mongo_password: Optional[str] = None

    scanned_directories = {"/data"}
    video_extensions = {".mp4", ".mkv", ".flv", ".avi"}

    concurrent_videos = 4
    redis_url = "redis://localhost"
    message_compression_level = 3

    minimum_confidence_shown = 0.75

    class Config:
        pass


settings = Settings()
