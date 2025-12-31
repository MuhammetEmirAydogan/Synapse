from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    GOOGLE_API_KEY: str 
    
    class Config:
        env_file = ".env"

settings = Settings()