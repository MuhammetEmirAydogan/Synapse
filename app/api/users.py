from fastapi import APIRouter, Depends
from app.schemas import UserOut
from app.api.deps import get_current_user
from app.models.sql import User

router = APIRouter()

# --- KULLANICI PROFİLİ GETİR  ---
@router.get("/me", response_model=UserOut)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user