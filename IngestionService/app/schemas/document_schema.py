from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DocumentSchema(BaseModel):
    id: UUID
    title: str
    content: str

class DocumentCreateSchema(BaseModel):
    title: str
    content: str

class DocumentUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
