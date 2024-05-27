from fastapi import FastAPI
from ..middlewares.cors_middleware import add_cors_middleware
from ..routers import document_router

app = FastAPI()

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(document_router.router, prefix="/api/v1")

@app.on_event("shutdown")
def shutdown():
    driver.close()
