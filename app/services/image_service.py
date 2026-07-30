from pathlib import Path
from PIL import Image
from app.core.config import settings


def create_thumbnail(
    image_path: Path,
) -> str:

    Path(settings.THUMBNAIL_DIR).mkdir(
        exist_ok=True
    )

    thumbnail_name = (
        f"thumb_{image_path.name}"
    )

    thumbnail_path = (
        Path(settings.THUMBNAIL_DIR)
        / thumbnail_name
    )

    with Image.open(image_path) as image:
        image.thumbnail((300, 300))
        image.save(thumbnail_path)

    return str(thumbnail_path)