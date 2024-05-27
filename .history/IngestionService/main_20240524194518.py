import logging
from fastapi import FastAPI
from app.routers.document_router import router as document_router
from neo4j import GraphDatabase
from app.utils.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG with KG", docs_url="/docs", root_path="/")

# Log when including routers
logger.info("Including document router.")
try:
    '''app.include_router(document_router, prefix="/api")
    logger.info("Document router included successfully.")'''
    router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


app.include_router(router)
except AttributeError as e:
    logger.error("Error including document router: %s", e)

# Initialize Neo4j database connection
logger.info("Initializing Neo4j driver.")
driver = GraphDatabase.driver(
    settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

# Dependency to provide database session to other parts of the app
def get_db_session():
    logger.info("Getting DB session.")
    with driver.session() as session:
        yield session

if __name__ == '__main__':
    import uvicorn
    logger.info("Starting server.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
