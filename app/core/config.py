import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "dev")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")

    DB_NAME: str = os.getenv("DB_NAME", "drugstore")
    DB_USER: str = os.getenv("DB_USER", "druguser")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "drugpass")
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
