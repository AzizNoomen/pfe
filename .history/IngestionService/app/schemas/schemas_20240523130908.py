from pydantic import BaseModel

class DocumentSchema(BaseModel):
    id: str
    title: str
    content: str

    class Config:
        orm_mode = True
