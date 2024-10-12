import httpx
from typing import List
from fastapi import UploadFile
from configuration.logging import logger


class IngestionService:
    
    async def upload_documents(self, files: List[UploadFile], chunking_method:str = 'regular', model_name:str = 'zephyr:latest') -> None:
        files_to_upload = [("files", (file.filename, await file.read(), file.content_type)) for file in files]
        try:

            async with httpx.AsyncClient(timeout=20000) as client:
                response = await client.post(
                    "http://ingestion-service:8001/api/ingestion_service/documents",
                    files=files_to_upload,
                    params={"chunking_method": chunking_method, "model_name": model_name}
                )
                response.raise_for_status()
                results = response.json()
                return results
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Error while making request: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise