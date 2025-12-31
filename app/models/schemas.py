from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    model_type: str = "flash"  

class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []
    used_model: str 