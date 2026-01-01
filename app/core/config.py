import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Synapse API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # --- KRİTİK EKLEME ---
    GOOGLE_API_KEY: str

    # GÜVENLİK AYARLARI
    SECRET_KEY: str = "cok_gizli_ve_uzun_rastgele_bir_metin_buraya_gelecek_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
    
        env_file = ".env"
        case_sensitive = True

settings = Settings()