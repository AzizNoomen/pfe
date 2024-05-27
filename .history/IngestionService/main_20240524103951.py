from fastapi import FastAPI
from app.middlewares.cors_middleware import add_cors_middleware
from app.routers import document_router

app = FastAPI(title="RAG with KG", docs_url="/docs", root_path="/")

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(document_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    Server(Config(
        app=app,
        host=app_config.APP_HOST,
        port=app_config.APP_PORT, log_config=logging_config,
        workers=app_config.NB_OF_WORKERS
    )).run()