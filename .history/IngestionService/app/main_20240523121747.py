from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from pydantic import BaseModel
from typing import List

from .config import settings
from .crud import create_node, get_nodes
from .models import Document

app = FastAPI()


driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

@app.post("/documents/", response_model=Document)
async def ingest_document(document: Document):
    with driver.session() as session:
        success = create_node(session, document)
        if not success:
            raise HTTPException(status_code=500, detail="Error ingesting document")
    return document

@app.get("/documents/")
async def get_document():
    with driver.session() as session:
        results = get_nodes(session, document)
        if not results:
            raise HTTPException(status_code=500, detail="Error ingesting document")
    return results

@app.on_event("shutdown")
def shutdown():
    driver.close()
