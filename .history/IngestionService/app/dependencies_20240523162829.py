from fastapi import Depends
from neo4j import GraphDatabase, Session
from app.utils.config import settings

def get_db_session() -> Session:
    driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
    return driver.session()

# You can add more dependencies here if needed
