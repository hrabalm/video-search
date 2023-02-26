import periodiq

from backend.tasks import dramatiq


@dramatiq.actor(periodic=periodiq.cron("0 * * * *"))
def stub_hourly_task():
    pass
