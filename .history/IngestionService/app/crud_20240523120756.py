from neo4j import Session
from .models import Document

def create_node(session: Session, document: Document) -> bool:
    query = """
    CREATE (d:Document {id: $id, title: $title, content: $content})
    """
    try:
        session.run(query, id=document.id, title=document.title, content=document.content)
        return True
    except Exception as e:
        print(f"Error creating node: {e}")
        return False

