from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.vector_db import get_vector_store
from app.core.config import settings

# Güncelleme: source_file parametresi eklendi
def get_answer(question: str, model_type: str = "flash", source_file: str = None):
    
    # 1. Model Seçimi (Senin çalışan 2.5 modellerin)
    if model_type == "pro":
        model_name = "gemini-2.5-pro"
    else:
        model_name = "gemini-2.5-flash"

    print(f"Model: {model_name} | Hedef Dosya: {source_file if source_file else 'Tümü'}")

    # 2. Veritabanı ve Filtreleme
    db = get_vector_store()
    
    # FİLTRE MEKANİZMASI BURADA
    search_kwargs = {"k": 3}
    if source_file:
        # Eğer bir dosya adı geldiyse, sadece o 'source' etiketine sahip olanları getir
        search_kwargs["filter"] = {"source": source_file}
    
    # Aramayı yap
    docs = db.similarity_search(question, **search_kwargs)
    
    # Context (Bağlam) oluştur
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Bulunan kaynakları listele
    found_sources = list(set([doc.metadata.get("source", "Bilinmiyor") for doc in docs]))
    
    # 3. Gemini Hazırlığı
    llm = ChatGoogleGenerativeAI(
        model=model_name, 
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.3
    )
    
    # 4. Prompt
    prompt = f"""
    Sen yardımsever bir asistansın. Sadece aşağıdaki bağlamı kullanarak cevap ver.
    
    Bağlam ({'Tüm Dosyalar' if not source_file else source_file}):
    {context}
    
    Soru:
    {question}
    
    Cevap:
    """
    
    # Modeli Çalıştır
    response = llm.invoke(prompt)
    
    return response.content, found_sources, model_name