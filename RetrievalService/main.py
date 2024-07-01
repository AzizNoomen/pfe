import logging
from fastapi import FastAPI
from app.middlewares.cors_middleware import middlewares
from app.routers.retrieval_router import router as retrieval_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Retrieval Service", middleware=middlewares)

try:
    app.include_router(retrieval_router, prefix="/api")
    logger.info("retrieval router included successfully.")
    

except AttributeError as e:
    logger.error("Error including retrieval router: %s", e)


if __name__ == '__main__':
    import uvicorn
    logger.info("Starting server.")
    uvicorn.run(app, host="0.0.0.0", port=8002)
