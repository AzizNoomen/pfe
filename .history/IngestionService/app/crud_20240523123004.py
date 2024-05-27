from neo4j import Session
from .models import Document
from typing import List

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

def fetch_all_nodes(session: Session) -> List[Document]:
    query = """
    MATCH (d:Document)
    RETURN d.id AS id, d.title AS title, d.content AS content
    """
    result = session.run(query)
    nodes = [Document(**record) for record in result]
    return nodes