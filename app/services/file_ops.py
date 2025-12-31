import os
import shutil
from fastapi import UploadFile

# Dosyaların kaydedileceği ana klasör
UPLOAD_DIR = "data"

# Eğer klasör yoksa oluştur 
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:

    # 1. Kaydedilecek dosya yolunu oluştur 
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 2. Dosyayı diske yaz 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return file_path