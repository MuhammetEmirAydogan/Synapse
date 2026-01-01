import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Bunlar standart kalabilir
    PROJECT_NAME: str = "Synapse API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    GOOGLE_API_KEY: str

    # Diğer ayarlar
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()