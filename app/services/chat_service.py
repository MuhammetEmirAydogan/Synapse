from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from app.services.vector_db import get_vector_store
from app.core.config import settings

def get_answer(question: str, model_type: str = "flash"):
    # 1. Model Seçimi 
    if model_type == "pro":
        # Listendeki en baba model
        model_name = "gemini-2.5-pro"
    else:
        # Listendeki en hızlı ve güncel flash model
        model_name = "gemini-2.5-flash"

    print(f"Seçilen Model: {model_name}")

    # 2. Veritabanına Bağlan ve Ara
    db = get_vector_store()
    # Benzerlik araması yap
    docs = db.similarity_search(question, k=3)
    
    # Context (Bağlam) oluştur
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Hangi dosyalardan bulduğunu not al
    sources = list(set([doc.metadata.get("source", "Bilinmiyor") for doc in docs]))
    
    # 3. Gemini Modelini Hazırla
    llm = ChatGoogleGenerativeAI(
        model=model_name, 
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.3
    )
    
    # 4. Prompt'u Hazırla
    prompt = f"""
    Sen yardımsever bir asistansın. Aşağıdaki bağlamı (Context) kullanarak soruyu cevapla.
    Eğer cevap bağlamda yoksa, dürüstçe "Bu konuda bilgim yok" de, uydurma.
    
    Bağlam:
    {context}
    
    Soru:
    {question}
    
    Cevap:
    """
    
    # 5. Modeli Çalıştır
    response = llm.invoke(prompt)
    
    return response.content, sources, model_name