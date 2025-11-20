"""
Configuration settings for the application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application settings loaded from environment variables.
    """
    # pylint: disable=too-few-public-methods
    ENV: str = os.getenv("ENV", "dev")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")

    DB_NAME: str = os.getenv("DB_NAME", "drugstore")
    DB_USER: str = os.getenv("DB_USER", "druguser")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "drugpass")
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    @property
    def database_url(self) -> str:
        """
        Constructs the database URL from environment variables.
        """
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
