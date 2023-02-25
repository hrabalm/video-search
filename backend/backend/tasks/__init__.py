import dramatiq
import dramatiq.brokers.redis
import dramatiq.results
import dramatiq.results.backends

import backend.dramatiq_extensions
import backend.tasks.settings as settings

tasks_settings = settings.Settings()
redis_url = tasks_settings.redis_url

message_encoder = backend.dramatiq_extensions.ZstdPickleEncoder(
    tasks_settings.compression_level
)
result_encoder = backend.dramatiq_extensions.ZstdPickleEncoder(
    tasks_settings.compression_level
)

redis_broker = dramatiq.brokers.redis.RedisBroker(url=redis_url)
redis_result = dramatiq.results.backends.RedisBackend(
    url=redis_url, encoder=result_encoder
)
redis_broker.add_middleware(dramatiq.results.Results(backend=redis_result))
dramatiq.set_broker(redis_broker)
dramatiq.set_encoder(message_encoder)
