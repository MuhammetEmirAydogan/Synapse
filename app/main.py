from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router  

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# --- Router Entegrasyonu ---
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def health_check():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "active"
    }