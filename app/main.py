from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router
from app.core.database import engine, Base
from app.models import sql 

# Uygulama başlarken Veritabanı Tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# --- CORS AYARLARI  ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router Entegrasyonu ---
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def health_check():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "active",
        "database": "PostgreSQL Connected "
    }