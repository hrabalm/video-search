import logging
import pathlib

from backend.tasks import dramatiq


@dramatiq.actor(time_limit=24 * 60 * 60 * 1_000)
def rpc_index_new_files(directories: list[str], extensions: list[str]):
    import backend.indexing

    if backend.indexing.IndexingController.try_start_indexing():
        logging.info("Indexing started.")
        backend.indexing.index_new_files(directories, extensions)
        backend.indexing.IndexingController.finish_indexing()
    else:
        logging.info("Cannot start logging, it is already on progress.")


@dramatiq.actor(time_limit=24 * 60 * 60 * 1_000)
def rpc_reindex_all(directories: list[str], extensions: list[str]):
    import backend.indexing

    if backend.indexing.IndexingController.try_start_indexing():
        logging.info("Indexing started.")
        backend.indexing.reindex_all(directories, extensions)
        backend.indexing.IndexingController.finish_indexing()
    else:
        logging.info("Cannot start logging, it is already on progress.")


@dramatiq.actor(time_limit=24 * 60 * 60 * 1_000, store_results=True)
def rpc_create_video_thumbnails(filepath: pathlib.Path):
    import backend.thumbnail
    from backend.api.db import fs

    keys = []
    for thumbnail in backend.thumbnail.create_thumbnails(filepath, 10, 1280, 720):
        key = fs.put(thumbnail)
        keys.append(key)
    return list(map(str, keys))
