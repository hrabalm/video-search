import dramatiq
import dramatiq.brokers.redis
import dramatiq.rate_limits.backends
import dramatiq.results
import dramatiq.results.backends
import periodiq

import backend.dramatiq_extensions
from backend.settings import settings

redis_url = settings.redis_url

message_encoder = backend.dramatiq_extensions.ZstdPickleEncoder(
    settings.message_compression_level
)
result_encoder = backend.dramatiq_extensions.ZstdPickleEncoder(
    settings.message_compression_level
)

redis_broker = dramatiq.brokers.redis.RedisBroker(url=redis_url)
redis_result = dramatiq.results.backends.RedisBackend(
    url=redis_url, encoder=result_encoder
)
redis_broker.add_middleware(
    dramatiq.results.Results(backend=redis_result, result_ttl=60 * 60 * 1_000)
)
redis_broker.add_middleware(periodiq.PeriodiqMiddleware())
dramatiq.set_broker(redis_broker)
dramatiq.set_encoder(message_encoder)

rate_limit_backend = dramatiq.rate_limits.backends.RedisBackend(url=redis_url)
