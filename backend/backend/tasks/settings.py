import pydantic


class Settings(pydantic.BaseSettings):
    redis_url = "redis://localhost"