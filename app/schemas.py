from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. TOKEN KALIBI
class Token(BaseModel):
    access_token: str
    token_type: str

# 2. KAYIT OLURKEN İSTENEN VERİLER
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company_name: str 

# 3. KULLANICI BİLGİSİ GÖSTERİRKEN
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    company_id: int

    class Config:
        from_attributes = True  

class UserLogin(BaseModel):
    email: EmailStr
    password: str