from fastapi import FastAPI
from .app.middlewares.cors_middleware import add_cors_middleware
from .app.routers import document_router

app = FastAPI(title="RAG with KG",
                docs_url="/docs",
            )

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(document_router.router, prefix="/api/")

@app.on_event("shutdown")
def shutdown():
    driver.close()
