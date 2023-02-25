import dramatiq

import backend.indexing


@dramatiq.actor
def reindex_all(directories: list[str], extensions: list[str]):
    backend.indexing.reindex_all(directories, extensions)
