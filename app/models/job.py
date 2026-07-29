from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    original_filename: Mapped[str] = mapped_column(String)

    stored_filename: Mapped[str] = mapped_column(String)

    status: Mapped[str] = mapped_column(
        String,
        default="queued",
    )

    thumbnail_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )