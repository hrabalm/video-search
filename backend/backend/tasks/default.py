from backend.tasks import dramatiq


@dramatiq.actor
def rpc_reindex_all(directories: list[str], extensions: list[str]):
    import backend.indexing

    backend.indexing.reindex_all(directories, extensions)
