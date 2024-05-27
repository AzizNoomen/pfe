import logging
from fastapi import FastAPI
from app.routers.document_router import router as document_router
from app.middlewares.cors_middleware import middlewares
from app.helpers.db_helpers import Neo4jHelper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG with KG", middleware=middlewares)

# Log when including routers
logger.info("Including document router.")

try:
    app.include_router(document_router, prefix="/api")
    logger.info("Document router included successfully.")

except AttributeError as e:
    logger.error("Error including document router: %s", e)

neo4j_helper = Neo4jHelper(uri="neo4j://localhost:7687", user="neo4j", password="aziz1234)

# Initialize database
def get_db_session():
    logger.info("Getting Neo4j session.")
    return Neo4jHelper

if __name__ == '__main__':
    import uvicorn
    logger.info("Starting server.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
