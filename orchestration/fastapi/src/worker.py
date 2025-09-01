from celery import Celery, Task

from settings import settings


class TaskRetry(Task):
    autoretry_for = [Exception]
    retry_kwargs = {"max_retries": 1}
    retry_backoff = True
    serializer = "pickle"


worker = Celery(
    broker=settings.redis.dsn,
    backend=settings.redis.dsn,
    include=["tasks"],
    task_cls=TaskRetry,
)

worker.conf.update(
    timezone="UTC",
    task_ignore_result=True,
    task_default_queue="default",
    accept_content={"json", "pickle"},
    worker_pool="threads",
)
