import uuid
import pandas as pd
import numpy as np
from .prompts import graphPrompt
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query2Dataframe(query) -> pd.DataFrame:
    row = {
        "text": query
    }
    df = pd.DataFrame([row])
    return df


async def query2Graph(dataframe: pd.DataFrame, model=None) -> list:
    
    try:
        async def apply_async(row):
            return await graphPrompt(row.text, {}, model)

        tasks = [apply_async(row) for _, row in dataframe.iterrows()]
        
        results = await asyncio.gather(*tasks)
        
        # Drop None values (in case of errors in graphPrompt)
        results = [result for result in results if result is not None]
        
        if len(results) > 1:
            # Flatten the list of lists to one single list of entities.
            concept_list = np.concatenate(results).ravel().tolist()
        
        elif len(results) == 1:
            print("Single row dataframe.")
            concept_list = results[0]

        else:
            print(f"No results after dropping NaN on attempt")
            concept_list = []
        
        return concept_list
        
    except Exception as e:
        logger.error(f"Error in df2Graph: {e}", exc_info=True)
        raise e
    

async def graph2Df(nodes_list) -> pd.DataFrame:
    ## Remove all NaN entities
    graph_dataframe = pd.DataFrame(nodes_list).replace(" ", np.nan)
    graph_dataframe = graph_dataframe.dropna(subset=["node_1", "node_2"])
    graph_dataframe["node_1"] = graph_dataframe["node_1"].apply(lambda x: x.lower())
    graph_dataframe["node_2"] = graph_dataframe["node_2"].apply(lambda x: x.lower())

    return graph_dataframe


