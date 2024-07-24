from fastapi import FastAPI
from uvicorn import Server, Config

from configuration.injection_container import DependencyContainer
from configuration.config import app_config
from app.middlewares.cors_middleware import middlewares
from app.routers.ingestion_router import router as ingestion_router


app = FastAPI(title=app_config.APP_TITLE, middleware=middlewares)

app.container = DependencyContainer()
app.container.db_helpers().init_database()

app.include_router(ingestion_router, prefix="/api", tags=["Ingestion"])


if __name__ == '__main__':
    Server(Config(app=app,
                    host=app_config.APP_HOST,
                    port=app_config.APP_PORT)).run()
