import os


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "ocr-api-server")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    USE_GPU: bool = os.getenv("USE_GPU", "false").lower() == "true"
    OCR_LANG: str = os.getenv("OCR_LANG", "en")
    OCR_USE_ANGLE_CLS: bool = os.getenv("OCR_USE_ANGLE_CLS", "true").lower() == "true"

    TMP_DIR: str = os.getenv("TMP_DIR", "/tmp/ocr-api")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))


settings = Settings()