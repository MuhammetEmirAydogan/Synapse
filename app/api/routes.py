from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_ops import save_upload_file
from app.services.pdf_loader import load_pdf_text
from app.services.splitter import chunk_text
from app.services.vector_db import add_texts_to_db

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyaları yüklenebilir.")
    
    try:
        # 1. Kaydet
        file_path = await save_upload_file(file)
        
        # 2. Oku
        full_text = load_pdf_text(file_path)
        
        # 3. Parçala
        chunks = chunk_text(full_text)
        
        # 4. Veritabanına Göm (Vector Embedding)
        metadatas = [{"source": file.filename} for _ in chunks]
        
        success = add_texts_to_db(chunks, metadatas)
        
        return {
            "filename": file.filename,
            "total_chunks": len(chunks),
            "status": "Vector Database'e başarıyla kaydedildi!",
            "db_success": success
        }
    except Exception as e:
        print(f"Hata detayı: {e}") 
        raise HTTPException(status_code=500, detail=str(e))