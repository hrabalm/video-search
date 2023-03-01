import logging
import pathlib

from dramatiq.rate_limits import ConcurrentRateLimiter

from backend.tasks import dramatiq, rate_limit_backend

INDEXING_DISTRIBUTED_MUTEX = ConcurrentRateLimiter(
    backend=rate_limit_backend, key="indexing", limit=1
)


@dramatiq.actor(time_limit=24 * 60 * 60 * 1_000)
def rpc_index_new_files(directories: list[str], extensions: list[str]):
    with INDEXING_DISTRIBUTED_MUTEX.acquire(raise_on_failure=False) as acquired:
        if not acquired:
            logging.info("(Lock)Cannot start logging, it is already on progress.")
            return
        import backend.indexing

        logging.info("Indexing started.")
        backend.indexing.index_new_files(directories, extensions)


@dramatiq.actor(time_limit=24 * 60 * 60 * 1_000)
def rpc_reindex_all(directories: list[str], extensions: list[str]):
    with INDEXING_DISTRIBUTED_MUTEX.acquire(raise_on_failure=False) as acquired:
        if not acquired:
            logging.info("(Lock)Cannot start logging, it is already on progress.")
            return
        import backend.indexing

        logging.info("Indexing started.")
        backend.indexing.reindex_all(directories, extensions)


@dramatiq.actor(time_limit=24 * 60 * 60 * 1_000, store_results=True)
def rpc_create_video_thumbnails(filepath: pathlib.Path):
    import backend.thumbnail
    from backend.api.db import fs

    keys = []
    for thumbnail in backend.thumbnail.create_thumbnails(filepath, 10, 1280, 720):
        key = fs.put(thumbnail)
        keys.append(key)
    return list(map(str, keys))
