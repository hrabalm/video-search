import periodiq

from backend.tasks import dramatiq


@dramatiq.actor(periodic=periodiq.cron("0 * * * *"))
def stub_hourly_task():
    pass


@dramatiq.actor(periodic=periodiq.cron("* * * * *"))
def index_new_files():
    from backend.settings import settings
    from backend.tasks.default import rpc_index_new_files

    directories = list(settings.scanned_directories)
    extensions = list(settings.video_extensions)
    rpc_index_new_files.send(directories, extensions)
