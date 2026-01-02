import os
from pypdf import PdfReader
from docx import Document

def load_document_text(file_path: str) -> str:
    # Dosya uzantısını al 
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _read_pdf(file_path)
    elif ext == ".docx":
        return _read_docx(file_path)
    elif ext == ".txt":
        return _read_txt(file_path)
    else:
        # Desteklenmeyen bir türse hata ver
        raise ValueError(f"Desteklenmeyen dosya formatı: {ext}")

# --- GİZLİ YARDIMCI FONKSİYONLAR ---

def _read_pdf(path):
    text = ""
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
    return text

def _read_docx(path):
    text = ""
    try:
        doc = Document(path)
        # Word belgelerinde metin paragraflar halindedir
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Word okuma hatası: {e}")
    return text

def _read_txt(path):
    try:
        # utf-8 formatında okumaya çalış, Türkçe karakter sorunu olmasın
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"TXT okuma hatası: {e}")
        return ""