from fastapi import FastAPI
from uvicorn import Server, Config

from configuration.dependencies import DependencyContainer
from configuration.config import app_config
from app.middlewares.cors_middleware import middlewares
from app.routers.ollama_router import router as ollama_router


app = FastAPI(title=app_config.APP_TITLE, middleware=middlewares)

app.container = DependencyContainer()

app.include_router(ollama_router, prefix="/api", tags=["Ollama"])

if __name__ == '__main__':
    Server(Config(app=app,
                    host=app_config.APP_HOST,
                    port=app_config.APP_PORT)).run()