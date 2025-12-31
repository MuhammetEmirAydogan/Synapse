import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

# 1. Embedding Modelini Hazırla
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=settings.GOOGLE_API_KEY
)

# 2. Vektör Veritabanı Ayarları
PERSIST_DIRECTORY = "chroma_db"

def get_vector_store():
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )
    return vector_store

def add_texts_to_db(texts: list, metadatas: list, batch_size: int = 10):
    db = get_vector_store()
    
    total_docs = len(texts)
    
    for i in range(0, total_docs, batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_metadatas = metadatas[i : i + batch_size]
        
        print(f"Batch işleniyor: {i} - {i + len(batch_texts)} arası...")
        
        db.add_texts(texts=batch_texts, metadatas=batch_metadatas)
        # Rate limit koruması
        time.sleep(2)
        
    return True