from pydantic import BaseModel
from typing import List
from typing import Any, List, Dict

class RetrievalResult(BaseModel):
    node_1: str
    relationship: str
    node_2: str
    score: float
    context: List[str] = []

class GenerationResponse(BaseModel):
    answer: str
