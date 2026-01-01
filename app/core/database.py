from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Docker-Compose dosyasındaki bilgilerle eşleşen adres:
SQLALCHEMY_DATABASE_URL = "postgresql://synapse_user:synapse_password@localhost:5433/synapse_db"

# Motoru Bağla
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Oturum Yöneticisi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Sınıfı (Tablolar buna miras verecek)
Base = declarative_base()

# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()