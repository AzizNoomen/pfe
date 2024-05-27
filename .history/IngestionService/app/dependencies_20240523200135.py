from fastapi import Depends
from neo4j import GraphDatabase, Session
from app.utils.config import settings

def get_db_session() -> Session:
    try:
        session = driver.session()
        yield session
    finally:
        session.close()