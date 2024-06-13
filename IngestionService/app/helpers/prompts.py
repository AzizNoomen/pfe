import httpx
import json
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def graphPrompt(input: str, metadata={}, model="mistral-openorca:latest"):
    if model == None:
        model = "mistral-openorca:latest"

    #model_info = client.show(model_name=model)
    #print(chalk.blue(model_info), "\n")

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
        "and the relation between them, like the follwing: \n"
        "[\n"
        "   {\n"
        '       "node_1": "A concept from extracted ontology",\n'
        '       "node_2": "A related concept from extracted ontology",\n'
        '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences without repeating the information stated in either one of the nodes"\n'
        "   }, {...}\n"
        "]"
    )

    logger.info("got into graph prompt")

    USER_PROMPT = f"context: ```{input}``` \n\n output: "
    async with httpx.AsyncClient(timeout=20000) as client:
        response = await client.post(f"http://model-service:8001/ollama/generate_text", json = {"model_name": model, "system": SYS_PROMPT, "prompt": USER_PROMPT})
        if response.status_code == 200:
            logger.info("response from model service",)
        else:
            logger.error("Error in response from model service. Status code:", response.status_code, "Content:", response.content)

    try:
        result = response.json()
        result = [dict(item, **metadata) for item in result]
        print("result from llm:", result)

    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result



async def generationPrompt(Semantic_search_results, query, model="mistral-openorca:latest"):

    if model is None:
        model = "mistral-openorca:latest"

    # Define the system prompt for the language model
    SYS_PROMPT = (
        "You are a language model who generates a response based on the given input.\n"
        "The input consists of a list of relationships between nodes, with a score and a context list for each relationship.\n"
        "The score represents the cosine similarity between the query and the corresponding node in the database, which is used for retrieval in a Retrieval-Augmented Generation (RAG) system.\n"
        "The context list is a list of nodes that are related to the source and target nodes of the relationship, and provide additional context and information about the relationship.\n"
        "Your task is to generate a coherent and meaningful summary of the information contained in the relationships and their context lists, in the context of the original query.\n"
        "Do not mention any technical details about the relationships, nodes, scores, or context in your response. Just provide a summary of the information.\n"
        "Format your output as a single string.\n"
    )

    # Define the user prompt for the language model
    USER_PROMPT = f"input: {Semantic_search_results.to_string(index=False)}\nOriginal query: {query}"

    # Generate a response using the language model
    async with httpx.AsyncClient(timeout=200) as client:
        response = await client.post("http://Model-Service:8001/ollama/generate_text", json={"model_name": model, "system": SYS_PROMPT, "prompt": USER_PROMPT})

    try:
        result = json.loads(response)
        result = [dict(iter, **input)]
    except Exception as e:
        #print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        #print("Exception:", e)  # Print the exception for further debugging
        result = None

    return result
