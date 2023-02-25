from backend.tasks import redis_broker, redis_result, dramatiq


@dramatiq.actor(
    queue_name="ml", store_results=True, broker=redis_broker, result_ttl=30 * 1_0000
)
def remote_classify_batch(images, classifier_name: str):
    from backend.tagging.perframe import classify_batch as f

    return f(images, classifier_name)
