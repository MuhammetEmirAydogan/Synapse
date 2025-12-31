from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_ops import save_upload_file
from app.services.pdf_loader import load_pdf_text
from app.services.splitter import chunk_text

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
        
        return {
            "filename": file.filename,
            "total_text_length": len(full_text),
            "total_chunks": len(chunks), 
            "first_chunk_preview": chunks[0] 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))