from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_ops import save_upload_file
from app.services.pdf_loader import load_pdf_text
from app.services.splitter import chunk_text
from app.services.vector_db import add_texts_to_db
# DİKKAT: Artık QueryRequest değil, ChatRequest kullanıyoruz
from app.models.schemas import ChatRequest, ChatResponse 
from app.services.chat_service import get_answer

router = APIRouter()

# 1. DOSYA YÜKLEME
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyaları yüklenebilir.")
    
    try:
        # Dosyayı kaydet
        file_path = await save_upload_file(file)
        
        # Oku ve Parçala
        full_text = load_pdf_text(file_path)
        chunks = chunk_text(full_text)
        
        # Veritabanına kaydet (Burada source=dosya_adi ekleniyor, bu önemli!)
        metadatas = [{"source": file.filename} for _ in chunks]
        success = add_texts_to_db(chunks, metadatas)
        
        return {
            "filename": file.filename,
            "total_chunks": len(chunks),
            "status": "Vector Database'e başarıyla kaydedildi!",
            "db_success": success
        }
    except Exception as e:
        print(f"Upload Hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 2. SORU SORMA 
@router.post("/ask", response_model=ChatResponse)
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