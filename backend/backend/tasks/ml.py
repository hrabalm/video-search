from backend.tasks import dramatiq


@dramatiq.actor(queue_name="ml", store_results=True)
def rpc_classify_batch(images, classifier_name: str):
    from backend.tagging.perframe import classify_batch as f

    return f(images, classifier_name)
