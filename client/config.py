from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

class Config:
    """
    Хранитель окружных переменных.
    Значения читаются из переменных окружения (или файла .env в корне проекта).
    """
    TOKEN = os.getenv("YANDEX_DISK_OAUTH_TOKEN")
    BASE_URL = os.getenv("YANDEX_DISK_BASE_URL", "https://cloud-api.yandex.net")

    @classmethod
    def validate(cls):
        if not cls.TOKEN:
            raise RuntimeError(
                "Не задан OAuth токен для Яндекс.Диска.\n"
                "Установите переменную окружения YANDEX_DISK_OAUTH_TOKEN "
                "(файл .env —> пример в .env.example)."
            )
