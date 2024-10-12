import httpx
from typing import Any, List, Dict
from configuration.logging import logger

class QnAService:
    
    async def retrieve(self, question: str, retrieval_model:str = "zephyr:latest", reranker:str = None) -> List[Dict[str, Any]]:
        
        logger.info("retrieval model: {}", retrieval_model)
        logger.info("reranker: {}", reranker)

        try:
            async with httpx.AsyncClient(timeout=2000) as client:
                response = await client.get(
                    "http://retrieval-service:8002/api/retrieval_service/related-documents",
                    params={"question": question, "model": retrieval_model, "top_n": 5, "similarity_threshold": 0.6, "reranker": reranker}
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
    

    async def generate(self, question: str, context: List[Dict[str, Any]], generation_model:str = "llama3:latest") -> str:
        
        logger.info("generation model: {}", generation_model)
        try:
            async with httpx.AsyncClient(timeout=2000) as client:
                response = await client.post(
                    "http://generation-service:8003/api/generation_service/answer",
                    params={"question": question,"model_name": generation_model}, json = context
                )
                response.raise_for_status()
                answer = response.json()['answer']
                return answer
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Error while making request: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise
