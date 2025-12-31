from pypdf import PdfReader

def load_pdf_text(file_path: str) -> str:
    text = ""
    try:
        reader = PdfReader(file_path)
        
        # Sayfa sayfa gez ve metinleri birleştirme
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
                
        return text
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        return ""