import shutil
import pandas as pd
import numpy as np
import os
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from pathlib import Path
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
from app.repositories.graph_repository import GraphRepository
from app.helpers.df_helpers import documents2Dataframe, df2Graph, graph2Df

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphService:
    def __init__(self):
        self.graph_repository = GraphRepository()
    
    def load_documents(self, uploaded_files: List[UploadFile]) -> pd.DataFrame:
        documents = []

        for uploaded_file in uploaded_files:
            if uploaded_file:
                # Save the uploaded file to a temporary path
                temp_path = Path(f"{uploaded_file.filename}")
                with open(temp_path, "wb") as buffer:
                    shutil.copyfileobj(uploaded_file.file, buffer)

                # Load the document using PyPDFLoader
                loader = PyPDFLoader(str(temp_path))
                documents.extend(loader.load())

                # Remove the temporary file
                os.remove(temp_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150,
            length_function=len,
            is_separator_regex=False,
        )

        pages = splitter.split_documents(documents)

        logger.info("Loaded documents: %d", len(pages))

        df = documents2Dataframe(pages)
        logger.info("Document dataframe created with shape: %s", df.shape)

        return df


    async def generate_graph(self, df: pd.DataFrame) -> pd.DataFrame:
        concepts_list = await df2Graph(df, model='zephyr:latest')
        logger.info("Concepts list created %s", len(concepts_list))
        dfg1 = graph2Df(concepts_list)

        logger.info("Concepts dataframe created with shape: %s", dfg1.shape)

        return dfg1


    def contextual_proximity(self, df:pd.DataFrame) -> pd.DataFrame:
        ## Melt the dataframe into a list of nodes
        dfg_long = pd.melt(
            df, id_vars=["chunk_id", "source"], value_vars=["node_1", "node_2"], value_name="node"
        )

        dfg_long.drop(columns=["variable"], inplace=True)

        # Self join with chunk id as the key will create a link between terms occuring in the same text chunk.
        dfg_wide = pd.merge(dfg_long, dfg_long, on=["chunk_id", "source"], suffixes=("_1", "_2"))

        # drop self loops
        self_loops_drop = dfg_wide[dfg_wide["node_1"] == dfg_wide["node_2"]].index
        dfg2 = dfg_wide.drop(index=self_loops_drop).reset_index(drop=True)

        # Drop self loops and reflexive edges
        dfg2 = dfg_wide[dfg_wide["node_1"] != dfg_wide["node_2"]].reset_index(drop=True)
        
        ## Group and count edges.
        dfg2 = (
            dfg2.groupby(["node_1", "node_2", "source"])
            .agg({"chunk_id": [",".join, "count"]})
            .reset_index()
        )
        dfg2.columns = ["node_1", "node_2", "source", "chunk_id", "count"]
        dfg2.replace("", np.nan, inplace=True)
        dfg2.dropna(subset=["node_1", "node_2"], inplace=True)

        # Drop edges with 1 count
        dfg2 = dfg2[dfg2["count"] != 1]

        # Create a set of existing edges
        existing_edges = set(zip(df["node_1"], df["node_2"]))

        # Create a new column in dfg_wide with the pair of nodes as tuples
        dfg_wide["node_pair"] = list(zip(dfg_wide["node_1"], dfg_wide["node_2"]))

        # Filter out the existing edges
        dfg_wide = dfg_wide[~dfg_wide["node_pair"].isin(existing_edges)]

        # Reset the index and group and count the edges
        dfg_wide.reset_index(drop=True, inplace=True)
        dfg2 = (
            dfg_wide.groupby(["node_1", "node_2", "source"])
            .agg({"chunk_id": [",".join, "count"]})
            .reset_index()
        )
        dfg2.columns = ["node_1", "node_2", "source", "chunk_id", "count"]
        dfg2.replace("", np.nan, inplace=True)
        dfg2.dropna(subset=["node_1", "node_2"], inplace=True)

        # Drop edges with 1 count
        dfg2 = dfg2[dfg2["count"] != 1]
        dfg2 = dfg2[dfg2["node_1"] != dfg2["node_2"]]
        dfg2["edge"] = "contextual proximity"
        return dfg2


    def merge_relationships(self, dfg1: pd.DataFrame, dfg2:pd.DataFrame) -> pd.DataFrame:
        dfg = pd.concat([dfg1, dfg2], axis=0)
        dfg = (
            dfg.groupby(["node_1", "node_2", "source", "edge"])
            .agg({'count': 'sum'})
            .reset_index()
        )
        return dfg
    

    async def contruct_graph(self, dfg: pd.DataFrame) -> None:
        nodes = pd.concat([dfg['node_1'], dfg['node_2']], axis=0).unique()
        self.graph_repository.add_nodes(nodes)
        await self.graph_repository.add_edges(dfg)