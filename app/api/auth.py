from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.database import get_db
from app.models.sql import User, Company
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas import UserCreate, Token, UserOut
from app.core.config import settings
from app.api.deps import get_current_user 

router = APIRouter()

# --- 1. KAYIT OL ---
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # A. Bu email daha önce alınmış mı?
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Bu email adresi zaten sistemde kayıtlı."
        )

    # B. Şirket Oluştur 
    new_company = Company(name=user_in.company_name)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    # C. Kullanıcıyı Oluştur 
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        company_id=new_company.id,
        role="admin" 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# --- 2. GİRİŞ YAP ---
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # A. Kullanıcıyı Bul
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # B. Şifre Kontrolü
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hatalı email veya şifre",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # C. Token Oluştur
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- 3. KULLANICI BİLGİLERİMİ GETİR ---
@router.get("/users/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user