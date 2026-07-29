from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL")

    UPLOAD_DIR = os.getenv("UPLOAD_DIR")
    THUMBNAIL_DIR = os.getenv("THUMBNAIL_DIR")


settings = Settings()