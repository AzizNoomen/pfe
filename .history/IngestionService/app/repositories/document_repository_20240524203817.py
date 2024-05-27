from neo4j import Driver, GraphDatabase, Session
from app.models.document_models import Document
from app.utils.config import settings
from typing import List

class DocumentRepository:
    def __init__(self, session: Session):
        self.driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
        self.session = self.driver.session()

    def create_document(self, title: str, content: str) -> Document:
        with self.session as session:
            result = session.run("CREATE (d:Document {title: $title, content: $content}) RETURN d", title=title, content=content)
            document = Document(id=document_id, title=title, content=content)
            return document

    def get_documents(self) -> List[Document]:
        with self.session as session:
            result = session.run("MATCH (d:Document) RETURN d")
            return [Document(title=record["d"]["title"], content=record["d"]["content"]) for record in result]

    def close(self):
        self.driver.close()
