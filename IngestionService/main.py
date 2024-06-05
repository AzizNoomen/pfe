import logging
from fastapi import FastAPI
from app.middlewares.cors_middleware import middlewares
from app.routers.document_router import router as document_router
from app.routers.ollama_router import router as ollama_router


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG with KG", middleware=middlewares)

try:
    app.include_router(document_router, prefix="/api")
    logger.info("Document router included successfully.")
    app.include_router(ollama_router, prefix="/ollama", tags=["Ollama"])


except AttributeError as e:
    logger.error("Error including document router: %s", e)


if __name__ == '__main__':
    import uvicorn
    logger.info("Starting server.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
