from fastapi import FastAPI
from uvicorn import Server, Config
from configuration.injection_container import DependencyContainer
from app.middlewares.cors_middleware import middlewares
from app.routers.generation_router import router as generation_router
from configuration.config import app_config


app = FastAPI(title=app_config.APP_TITLE, middleware=middlewares)

app.container = DependencyContainer()

app.include_router(generation_router, prefix="/api")


if __name__ == '__main__':
    Server(Config(app=app,
                    host=app_config.APP_HOST,
                    port=app_config.APP_PORT)).run()
