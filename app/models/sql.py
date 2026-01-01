import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

# --- ENUM Sınıfları ---
class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"     
    COMPANY_ADMIN = "company_admin" 
    EMPLOYEE = "employee"           

class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

# 1. ŞİRKET TABLOSU
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    
    # Şirket Kuralları
    max_users = Column(Integer, default=5) 
    is_active = Column(Boolean, default=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    users = relationship("User", back_populates="company")
    invitations = relationship("Invitation", back_populates="company")

# 2. KULLANICI TABLOSU
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")

# 3. DAVET TABLOSU 
class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False) 
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE) 
    
    # Davet Linki Güvenliği
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime) 
    is_used = Column(Boolean, default=False) 
    

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="invitations")
    
    created_at = Column(DateTime, default=datetime.utcnow)