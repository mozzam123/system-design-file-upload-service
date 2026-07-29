import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.job import Job


def save_uploaded_file(
    file: UploadFile,
    db: Session,
) -> Job:

    Path(settings.UPLOAD_DIR).mkdir(
        exist_ok=True
    )

    unique_filename = (
        f"{uuid.uuid4()}-{file.filename}"
    )

    file_path = (
        Path(settings.UPLOAD_DIR)
        / unique_filename
    )

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    job = Job(
        original_filename=file.filename,
        stored_filename=unique_filename,
        status="queued",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job