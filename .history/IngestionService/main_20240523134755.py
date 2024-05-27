from fastapi import FastAPI
from .app.middlewares.cors_middleware import add_cors_middleware
from .app.routers import document_router
from neo4j import GraphDatabase
from .app.utils.config import settings

app = FastAPI (title="RAG with KG",
                docs_url="/docs",
                root_path="/"
            )

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(document_router, prefix="/api/")

# Initialize Neo4j database connection
driver = GraphDatabase.driver(
    settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

# Dependency to provide database session to other parts of the app
def get_db_session():
    with driver.session() as session:
        yield session

# Include routes and other setup here
# For example, you might include something like:
# app.include_router(document_router)

# Close the database connection when the app shuts down
@app.on_event("shutdown")
async def shutdown_event():
    driver.close()