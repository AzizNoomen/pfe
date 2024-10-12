from fastapi import FastAPI
from uvicorn import Server, Config
from configuration.injection_container import DependencyContainer
from app.middlewares.cors_middleware import middlewares
from app.routers.ingestion_router import router as ingestion_router
from app.routers.qna_router import router as qna_router
from app.routers.graph_visualization_router import router as vis_router
from configuration.config import app_config


app = FastAPI(title=app_config.APP_TITLE, middleware=middlewares)

app.container = DependencyContainer()

app.include_router(ingestion_router, prefix="/api")
app.include_router(qna_router, prefix="/api")
app.include_router(vis_router, prefix="/api")


if __name__ == '__main__':
    Server(Config(app=app,
                    host=app_config.APP_HOST,
                    port=app_config.APP_PORT)).run()
