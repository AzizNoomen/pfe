from fastapi import Depends
from neo4j import GraphDatabase, Session
from app.utils.config import settings

driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

def get_db_session() -> Session:
    try:
        session = driver.session()
        yield session
    finally:
        session.close()