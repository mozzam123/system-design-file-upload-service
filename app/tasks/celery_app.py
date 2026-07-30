from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "file_upload_service",
    broker=settings.RABBITMQ_URL,
    include=["app.tasks.image_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)