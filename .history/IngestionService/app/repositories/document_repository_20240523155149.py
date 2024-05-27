from neo4j import Driver, GraphDatabase
from app.models.document_models import Document
from app.utils.config import settings
from tyoing

class DocumentRepository:
    def __init__(self):
        self.driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

    def create_document(self, title: str, content: str) -> Document:
        with self.driver.session() as session:
            result = session.run("CREATE (d:Document {title: $title, content: $content}) RETURN d", title=title, content=content)
            return Document(id=result.single()["d"]["id"], title=title, content=content)

    def get_documents(self) -> List[Document]:
        with self.driver.session() as session:
            result = session.run("MATCH (d:Document) RETURN d")
            return [Document(id=record["d"]["id"], title=record["d"]["title"], content=record["d"]["content"]) for record in result]

    def close(self):
        self.driver.close()
