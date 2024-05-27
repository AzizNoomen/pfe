from neo4j import Session
from .models import Document
from typing import List
from neo4j import Node
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

def get_nodes(session: Session) -> List[]:
    query = """
            MATCH (n)
            RETURN n
            """
    try:
        result = session.run(query)
        nodes = [r["n"] for r in result]
        return nodes
    except Exception as e:
        print(f"Error fetching nodes: {e}")
        return []
