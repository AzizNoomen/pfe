from dataclasses import dataclass
import uuid

@dataclass
class Document:
    id: uuid.UUID
    title: str
    content: str

    def __init__(self,title: str, content: str, id: uuid.UUID = None):
        self.id = id or uuid.uuid4()
        self.title = title
        self.content = content
