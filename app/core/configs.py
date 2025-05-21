from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    @classmethod
    def get_env(cls, key: str, default: str | None = None) -> str | None:
        return os.getenv(key, default)
    