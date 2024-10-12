from pydantic import BaseModel
from typing import List, Optional

class RetrievalResult(BaseModel):
    node_1: str
    relationship: str
    node_2: str

class HybridSearchResult(RetrievalResult):
    score: Optional[float] = None
    context: Optional[List[str]] = []
