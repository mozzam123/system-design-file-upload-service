from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.job import UploadResponse
from app.services.upload_service import save_uploaded_file

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
)
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    job = save_uploaded_file(
        file=file,
        db=db,
    )

    return UploadResponse(
        job_id=job.id,
        status=job.status,
    )