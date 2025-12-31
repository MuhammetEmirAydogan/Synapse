from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

# 1. ŞİRKET TABLOSU
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) 
    subscription_plan = Column(String, default="free") 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="company")

# 2. KULLANICI TABLOSU
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) 
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="employee") 
    
    # Hangi şirkette çalışıyor?
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    # İlişki: Kullanıcının şirketi
    company = relationship("Company", back_populates="users")