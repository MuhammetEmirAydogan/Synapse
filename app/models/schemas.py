from pydantic import BaseModel
from typing import Optional  

class ChatRequest(BaseModel):
    question: str
    model_type: str = "flash"
    file_name: Optional[str] = None 

class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []
    used_model: str