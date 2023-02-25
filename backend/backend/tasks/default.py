import dramatiq
import backend.tasks

@dramatiq.actor
def reindex_all(directories: list[str], extensions: list[str]):
    import backend.indexing
    backend.indexing.reindex_all(directories, extensions)
