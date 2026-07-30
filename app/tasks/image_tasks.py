from pathlib import Path
from app.core.config import settings
from celery.utils.log import get_task_logger

from app.db.database import SessionLocal
from app.models.job import Job
from app.services.image_service import create_thumbnail
from app.tasks.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task
def process_image(job_id: int):

    db = SessionLocal()

    try:

        job = db.get(Job, job_id)

        if job is None:
            return

        job.status = "processing"
        db.commit()

        image_path = Path(settings.UPLOAD_DIR) / job.stored_filename

        thumbnail = create_thumbnail(image_path)

        job.thumbnail_path = thumbnail
        job.status = "completed"

        db.commit()

        logger.info(
            f"Finished job {job.id}"
        )

    except Exception as e:

        job.status = "failed"
        job.error_message = str(e)

        db.commit()

        raise

    finally:
        db.close()