import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    """Central place for configuration."""

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    # Paths (can be overridden in .env)
    DB_PATH: str = os.getenv("DB_PATH", "data/marketing_bebidas.db")
    VECTOR_PATH: str = os.getenv("VECTOR_PATH", "data/vector_store")


settings = Settings()
