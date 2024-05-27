from fastapi import FastAPI
from app.middlewares.cors_middleware import add_cors_middleware
from app.routers import document_router

app = FastAPI(title="RAG with KG")

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(document_router.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)