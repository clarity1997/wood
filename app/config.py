from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/furniture_db"
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/v1/chat/completions"
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"

settings = Settings()
