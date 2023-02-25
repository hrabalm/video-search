from backend.tasks import dramatiq


@dramatiq.actor(queue_name="ml", store_results=True, result_ttl=30 * 1_000)
def remote_classify_batch(images, classifier_name: str):
    from backend.tagging.perframe import classify_batch as f

    return f(images, classifier_name)
