from fastapi.responses import JSONResponse
import httpx
from configuration.logging import logger

class GraphVis:
    
    async def vis(self) -> JSONResponse:

        try:
            async with httpx.AsyncClient(timeout=2000) as client:
                response = await client.get(
                    "http://retrieval-service:8002/api/retrieval_service/graph",
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