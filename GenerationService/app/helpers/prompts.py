import httpx
from typing import List
from typing import Any, List, Dict
import json
from configuration.logging import logger


async def generationPrompt(query: str, retrieved_context: List[Dict[str, Any]], model: str = "mistral-openorca:latest") -> str:
    if model is None:
        model = "mistral-openorca:latest"
        
    context_text = "\n".join([json.dumps(ctx) for ctx in retrieved_context])

    logger.info("\ncontext string: %s", context_text)

    # Define the system prompt for the language model
    SYS_PROMPT = (
        "You are a language model who generates a response based on the given context and the original query.\n"
        """Each context contains a list of:\n
        - node1: The starting point of the relationship, which is a keyword or synonym related to the question.\n
        - relationship: The connection or relationship between node1 and node2.\n
        - node2: The endpoint of the relationship, which is a keyword or synonym related to the question.\n
        - additional context information: A list of extra keywords that exist in the same context of node1 and node2.
        - score: represents the cosine similarity between each relationship and the query.\n"""
        "Your task is to generate a coherent and meaningful summary of the information contained in the relationships and their context lists, in the context of the original query.\n"
        "Do not mention any technical details about the relationships, nodes, scores, or context in your response. Just provide a summary of the information.\n"
        "Format your output as a single string.\n"
    )

    # Define the user prompt for the language model, including additional context information
    USER_PROMPT = f"""
        context: {context_text}\n
        Original query: {query}\n\n
    """

    async with httpx.AsyncClient(timeout=2000) as client:
        response = await client.post(f"http://model-service:8000/api/ollama/text-generation", json = {"model_name": model, "system": SYS_PROMPT, "prompt": USER_PROMPT})

    return response.content