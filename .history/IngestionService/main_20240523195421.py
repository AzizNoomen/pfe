from fastapi import FastAPI
from app.middlewares.cors_middleware import add_cors_middleware
from app.routers import document_router
from neo4j import GraphDatabase
from app.utils.config import settings
from app.

app = FastAPI (title="RAG with KG")

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(document_router.router)

# Initialize Neo4j database connection
driver = GraphDatabase.driver(
    settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

# Dependency to provide database session to other parts of the app
def get_db_session():
    with driver.session() as session:
        yield session

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)