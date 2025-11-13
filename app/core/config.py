from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = "CHANGE ME"
    JWT_REFRESH_SECRET_KEY: str = "CHANGE_ME_REFRESH"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 17
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./auth.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
