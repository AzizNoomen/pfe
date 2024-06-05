import uuid
import pandas as pd
import numpy as np
from .prompts import graphPrompt


def documents2Dataframe(documents) -> pd.DataFrame:
    rows = []
    for chunk in documents:
        row = {
            "text": chunk.page_content,
            **chunk.metadata,
            "chunk_id": uuid.uuid4().hex,
        }
        rows = rows + [row]

    df = pd.DataFrame(rows)
    return df


def query2Dataframe(query) -> pd.DataFrame:
    row = {
        "text": query
    }
    df = pd.DataFrame([row])
    return df


def df2Graph(dataframe: pd.DataFrame, model=None) -> list:
    # dataframe.reset_index(inplace=True)
    if (len(dataframe) > 1):
        results = dataframe.apply(
            lambda row: graphPrompt(row.text, {"chunk_id": row.chunk_id, "source":row.source}, model), axis=1
        )
        # invalid json results in NaN
        results = results.dropna()
        results = results.reset_index(drop=True)

        ## Flatten the list of lists to one single list of entities.
        concept_list = np.concatenate(results).ravel().tolist()
        return concept_list
    
    else:
        results = dataframe.apply(
            lambda row: graphPrompt(row.text, {} ,model), axis=1
        )
        # invalid json results in NaN
        results = results.dropna()
        results = results.reset_index(drop=True)
        concept_list = results.ravel().tolist()
        return concept_list


def graph2Df(nodes_list) -> pd.DataFrame:
    ## Remove all NaN entities
    graph_dataframe = pd.DataFrame(nodes_list).replace(" ", np.nan)
    graph_dataframe = graph_dataframe.dropna(subset=["node_1", "node_2"])
    graph_dataframe["node_1"] = graph_dataframe["node_1"].apply(lambda x: x.lower())
    graph_dataframe["node_2"] = graph_dataframe["node_2"].apply(lambda x: x.lower())

    return graph_dataframe


