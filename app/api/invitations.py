from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import secrets 
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.sql import User, Invitation, UserRole
from app.core.security import get_password_hash 
from app.schemas import InvitationCreate, InvitationOut, UserOut, InvitationAccept 
from app.api.deps import get_current_user 

router = APIRouter()

# --- 1. PERSONEL DAVET ET  ---
@router.post("/invite", response_model=InvitationOut)
def invite_employee(
    invitation_in: InvitationCreate, 
    current_user: UserOut = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # 1. YETKİ KONTROLÜ
    if current_user.role != UserRole.COMPANY_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Bu işlem için yetkiniz yok. Sadece şirket yöneticileri çalışan davet edebilir."
        )

    # 2. AYNI KİŞİYE TEKRAR DAVET ATILMASIN
    existing_user = db.query(User).filter(User.email == invitation_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı zaten sisteme kayıtlı.")
        
    existing_invite = db.query(Invitation).filter(
        Invitation.email == invitation_in.email, 
        Invitation.is_used == False
    ).first()
    
    if existing_invite:
        raise HTTPException(status_code=400, detail="Bu maile zaten aktif bir davet gönderilmiş.")

    # 3. DAVETİ OLUŞTUR
    invite_token = secrets.token_urlsafe(32) 
    
    new_invitation = Invitation(
        email=invitation_in.email,
        role=invitation_in.role, 
        token=invite_token,
        expires_at=datetime.utcnow() + timedelta(days=2), 
        company_id=current_user.company_id 
    )
    
    db.add(new_invitation)
    db.commit()
    db.refresh(new_invitation)
    
    return new_invitation

# --- 2. DAVETİ KABUL ET ---
@router.post("/accept-invite", response_model=UserOut)
def accept_invitation(accept_in: InvitationAccept, db: Session = Depends(get_db)):
    
    # A. Daveti Bul
    invitation = db.query(Invitation).filter(Invitation.token == accept_in.token).first()
    
    # B. Güvenlik Kontrolleri
    if not invitation:
        raise HTTPException(status_code=404, detail="Geçersiz veya hatalı davet kodu.")
    
    if invitation.is_used:
        raise HTTPException(status_code=400, detail="Bu davet kodu zaten kullanılmış.")
        
    if invitation.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Bu davetin süresi dolmuş.")

    # C. Kullanıcıyı Oluştur 
    new_user = User(
        email=invitation.email, 
        hashed_password=get_password_hash(accept_in.password), 
        full_name=accept_in.full_name,
        company_id=invitation.company_id, 
        role=invitation.role,
        is_active=True
    )
    
    # D. Daveti 'Kullanıldı' İşaretle ve Kaydet
    invitation.is_used = True
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# --- 3. DAVETLERİ LİSTELE  ---
@router.get("/", response_model=List[InvitationOut])
def get_company_invitations(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Yetki Kontrolü
    if current_user.role != UserRole.COMPANY_ADMIN:
        raise HTTPException(
            status_code=403, 
            detail="Bu listeyi görüntüleme yetkiniz yok."
        )

    invitations = db.query(Invitation).filter(
        Invitation.company_id == current_user.company_id
    ).all()
    
    return invitations