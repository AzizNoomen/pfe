from pydantic import BaseModel

class DocumentSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True
