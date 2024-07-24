from pydantic import BaseModel
from typing import List, Optional

class GraphResponse(BaseModel):
    message: str
    nodes_added: int
    edges_added: int
