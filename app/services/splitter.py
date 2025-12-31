from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text: str):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Her parça yaklaşık 1000 karakter olsun
        chunk_overlap=200  # Parçalar arası 200 karakterlik örtüşme olsun
    )
    
    chunks = splitter.split_text(text)
    return chunks