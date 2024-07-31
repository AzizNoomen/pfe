import httpx
from typing import List, Dict, Any
from configuration.logging import logger
from app.exceptions.service_exceptions import ModelServiceUnavailable

async def graphPrompt(input: str, metadata: Dict[str, Any] = {}, model_name: str = "zephyr:latest") -> List[Dict[str, Any]]:
    logger.info("Chosen model: {}", model_name)
    
    SYS_PROMPT = (
        "You are a network graph maker who extracts terms and their relations from a given context. "
        "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
        "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
        "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
            "\tTerms may include object, entity, location, organization, person, \n"
            "\tcondition, acronym, documents, service, concept, etc.\n"
            "\tTerms should be as atomistic as possible\n\n"
        "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
            "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
            "\tTerms can be related to many other terms\n\n"
        "Thought 3: Find out the relation between each such related pair of terms. \n\n"
        "Format your output as a list of json. Each element of the list contains a pair of terms"
        "and the relation between them, strictly like the follwing: \n"
        "[\n"
        "   {\n"
        '       "node_1": "A concept from extracted ontology",\n'
        '       "node_2": "A related concept from extracted ontology",\n'
        '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences without repeating the information stated in either one of the nodes"\n'
        "   }, {...}\n"
        "]"
    )

    logger.info("got into graph prompt")

    attempt = 0
    result = None
    max_retries = 3

    USER_PROMPT = f"context: ```{input}``` \n\n output: "

    while attempt < max_retries and result is None:

        try:
            async with httpx.AsyncClient(timeout=20000) as client:
                response = await client.post(f"http://model-service:8000/api/ollama/text-generation", json = {"model_name": model_name, "system": SYS_PROMPT, "prompt": USER_PROMPT})
                if response.status_code == 200:
                    logger.info("response from model service",)
                else:
                    logger.error("Error in response from model service. Status code:", response.status_code, "Content:", response.content)
        except httpx.HTTPStatusError:
                raise ModelServiceUnavailable()
        
        try:
            result = response.json()
            result = [dict(item, **metadata) for item in result]
            print("result from llm:", result)

        except:
            print(f"\n\nERROR ### Here is the buggy response (attempt {attempt + 1}): ", response, "\n\n")
            attempt += 1
            result = None

    return result
