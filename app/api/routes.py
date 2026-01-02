from fastapi import APIRouter, UploadFile, File, HTTPException
import os 
from app.services.file_ops import save_upload_file
from app.services.document_loader import load_document_text 
from app.services.splitter import chunk_text
from app.services.vector_db import add_texts_to_db
from app.services.chat_service import get_answer
from app.schemas import ChatRequest, ChatResponse

# API Modüllerini İçe Aktar
from app.api import auth, invitations, users

router = APIRouter()

# --- 1. AUTH MODÜLÜ ---
router.include_router(auth.router, tags=["Authentication"])

# --- 2. KULLANICI MODÜLÜ ---
router.include_router(users.router, prefix="/users", tags=["Users"])

# --- 3. KURUMSAL MODÜL ---
router.include_router(invitations.router, prefix="/invitations", tags=["Invitations"])

# --- 4. DOSYA YÜKLEME  ---
@router.post("/upload", tags=["Chat & Files"])
async def upload_document(file: UploadFile = File(...)):
    # 1. Uzantı Kontrolü 
    ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Desteklenmeyen format! Sadece şunlar yüklenebilir: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    try:
        # 2. Dosyayı diske kaydet
        file_path = await save_upload_file(file)
        
        # 3. Akıllı Loader ile metni oku 
        full_text = load_document_text(file_path)
        
        # Boş dosya kontrolü
        if not full_text.strip():
            raise HTTPException(status_code=400, detail="Dosya içeriği boş veya okunamadı.")

        # 4. Metni parçala
        chunks = chunk_text(full_text)
        
        # 5. Veritabanına kaydet
        metadatas = [{"source": file.filename} for _ in chunks]
        success = add_texts_to_db(chunks, metadatas)
        
        return {
            "filename": file.filename,
            "type": ext, 
            "total_chunks": len(chunks),
            "status": "Vector Database'e başarıyla kaydedildi!",
            "db_success": success
        }
    except Exception as e:
        print(f"Upload Hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- 5. SORU SORMA ---
@router.post("/ask", response_model=ChatResponse, tags=["Chat & Files"])
def ask_question(request: ChatRequest):
    try:
        answer, sources, used_model = get_answer(
            request.question, 
            request.model_type,
            request.file_name  
        )
        
        return ChatResponse(answer=answer, sources=sources, used_model=used_model)
    except Exception as e:
        print(f"Chat Hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))