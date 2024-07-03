import logging
from fastapi import FastAPI
from app.middlewares.cors_middleware import middlewares
from app.routers.ollama_router import router as ollama_router


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Model Service", middleware=middlewares)

try:
    app.include_router(ollama_router, prefix="/api", tags=["Ollama"])
    logger.info("Ollama router included successfully.")


except AttributeError as e:
    logger.error("Error including ollama router: %s", e)


if __name__ == '__main__':
    import uvicorn
    logger.info("Starting server.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
