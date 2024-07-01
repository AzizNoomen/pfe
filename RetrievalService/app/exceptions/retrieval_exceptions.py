from fastapi import HTTPException, status

class DatabaseNotInitialized(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database is not initialized")

class ModelServiceUnavailable(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model service is not available")
