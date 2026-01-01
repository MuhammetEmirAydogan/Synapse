from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.sql import UserRole, SubscriptionPlan 

# ==========================================
# 1. ESKİ CHAT ŞEMALARI
# ==========================================
class ChatRequest(BaseModel):
    question: str
    model_type: str = "flash"
    file_name: Optional[str] = None 

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    used_model: str

# ==========================================
# 2. TOKEN VE GÜVENLİK
# ==========================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ==========================================
# 3. KULLANICI VE ŞİRKET KAYIT ŞEMALARI
# ==========================================
class UserCreateWithCompany(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company_name: str 

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    role: UserRole 
    company_id: Optional[int] = None

    class Config:
        from_attributes = True 

# ==========================================
# 4. DAVET  ŞEMALARI 
# ==========================================
class InvitationCreate(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.EMPLOYEE

class InvitationOut(InvitationCreate):
    id: int
    token: str 
    is_used: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==========================================
# 5. ŞİRKET DETAY ŞEMASI
# ==========================================
class CompanyOut(BaseModel):
    id: int
    name: str
    subscription_plan: SubscriptionPlan
    is_active: bool
    
    class Config:
        from_attributes = True

# ==========================================
# 6. DAVET KABUL ETME 
# ==========================================
class InvitationAccept(BaseModel):
    token: str     
    password: str   
    full_name: str  