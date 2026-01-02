from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router
from app.core.database import engine, Base
import app.models.sql 

# Tabloları veritabanında oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- CORS AYARLARI ---
origins = [
    "http://localhost:5173",      
    "http://127.0.0.1:5173",      
    "http://localhost:3000",      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
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
        "database": "PostgreSQL Connected"
    }