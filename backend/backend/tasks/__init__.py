import dramatiq
import dramatiq.brokers.redis
import dramatiq.results
import dramatiq.results.backends

import backend.tasks.settings as settings

tasks_settings = settings.Settings()
redis_url = tasks_settings.redis_url

redis_broker = dramatiq.brokers.redis.RedisBroker(url=redis_url)
redis_result = dramatiq.results.backends.RedisBackend(
    url=redis_url, encoder=dramatiq.PickleEncoder()
)
redis_broker.add_middleware(dramatiq.results.Results(backend=redis_result))
dramatiq.set_broker(redis_broker)
dramatiq.set_encoder(dramatiq.PickleEncoder())
