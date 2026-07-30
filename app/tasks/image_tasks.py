from celery.utils.log import get_task_logger

from app.tasks.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task
def process_image(job_id: int):

    logger.info(
        f"Processing job {job_id}"
    )

    print(f"Processing job {job_id}")