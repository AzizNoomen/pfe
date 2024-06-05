from app.database import db
from app.models import Document
import logging
from uuid import UUID
from app.exceptions.service_exceptions import DatabaseConnectionError
from neo4j.exceptions import ServiceUnavailable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentRepository:
    def create(self, title, content):
        document = Document(title=title, content=content)
        try:
            with db.driver.session() as session:
                result = session.run(
                    "CREATE (d:Document {id: $id, title: $title, content: $content}) RETURN d",
                    {"id": str(document.id), "title": title, "content": content}
                )
                record = result.single()
                if record:
                    logger.info("Document created: %s", document)
                    return document
                else:
                    logger.error("Failed to create document")
                    return None
        except ServiceUnavailable:
            logger.error("Database is not available")
            raise DatabaseConnectionError()

    def get_by_id(self, id: UUID):
        try:
            with db.driver.session() as session:
                result = session.run(
                    "MATCH (d:Document) WHERE d.id = $id RETURN d",
                    {"id": str(id)}
                )
                record = result.single()
                if record:
                    doc_node = record["d"]
                    document = Document(id=UUID(doc_node["id"]), title=doc_node["title"], content=doc_node["content"])
                    logger.info("Document fetched: %s", document)
                    return document
                else:
                    logger.info("Document not found with id: %s", id)
                    return None
        except ServiceUnavailable:
            logger.error("Database is not available")
            raise DatabaseConnectionError()

    def update(self, id: UUID, title: str, content: str):
        try:
            with db.driver.session() as session:
                result = session.run(
                    "MATCH (d:Document) WHERE d.id = $id SET d.title = $title, d.content = $content RETURN d",
                    {"id": str(id), "title": title, "content": content}
                )
                record = result.single()
                if record:
                    document = self.get_by_id(id)
                    logger.info("Document updated: %s", document)
                    return document
                else:
                    logger.error("Failed to update document with id: %s", id)
                    return None
        except ServiceUnavailable:
            logger.error("Database is not available")
            raise DatabaseConnectionError()

    def delete(self, id: UUID):
        try:
            with db.driver.session() as session:
                session.run(
                    "MATCH (d:Document) WHERE d.id = $id DETACH DELETE d",
                    {"id": str(id)}
                )
                logger.info("Document deleted with id: %s", id)
        except ServiceUnavailable:
            logger.error("Database is not available")
            raise DatabaseConnectionError()

    def get_all(self):
        try:
            with db.driver.session() as session:
                result = session.run("MATCH (d:Document) RETURN d.id, d.title, d.content")
                documents = []
                for record in result:
                    documents.append(
                        Document(
                            id=UUID(record["d.id"]),
                            title=record["d.title"],
                            content=record["d.content"]
                        )
                    )
                return documents
        except ServiceUnavailable:
            logger.error("Database is not available")
            raise DatabaseConnectionError()
