from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

@app.get("/")
async def health_check():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "active"
    }