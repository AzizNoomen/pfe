import shutil
import pandas as pd
import numpy as np
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from pathlib import Path
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader,TextLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from app.repositories.ingestion_repository import IngestionRepository
from app.helpers.df_helpers import documents2Dataframe, df2Graph, graph2Df
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import HuggingFaceEmbeddings
from configuration.logging import logger


class IngestionService:
    def __init__(self, ingestion_repository: IngestionRepository):
        self.ingestion_repository = ingestion_repository
    
    def load_documents(self, uploaded_files: List[UploadFile]) -> List[dict]:
        documents = []

        for uploaded_file in uploaded_files:
            if uploaded_file:
                # Save the uploaded file to a temporary path
                temp_path = Path(f"{uploaded_file.filename}")
                with open(temp_path, "wb") as buffer:
                    shutil.copyfileobj(uploaded_file.file, buffer)

                if temp_path.suffix == ".pdf":
                    loader = PyPDFLoader(str(temp_path))
                elif temp_path.suffix == ".txt":
                    loader = TextLoader(str(temp_path))
                elif temp_path.suffix == ".docx":
                    loader = Docx2txtLoader(str(temp_path))
                elif temp_path.suffix == ".pptx":
                    loader = UnstructuredPowerPointLoader(str(temp_path))
                else:
                    logger.info(f"Unsupported file type: {temp_path.suffix}")
                    continue

                documents.extend(loader.load())
                # Remove the temporary file
                os.remove(temp_path)

        return documents
    
    def chunking(self, documents:List[dict], chunking_method:str = "regular") -> pd.DataFrame:

        if chunking_method == "regular":
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150,
                length_function=len,
                is_separator_regex=False,
            )

        elif chunking_method == "semantic":
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            splitter = SemanticChunker(embeddings=embeddings)
        
        else:
            raise ValueError(f"Unsupported chunking method: {chunking_method}")

        chunks = splitter.split_documents(documents)
        logger.info("number of chunks: %d", len(chunks))
        df = documents2Dataframe(chunks)
        logger.info("Document dataframe created with shape: %s", df.shape)

        return df


    async def generate_graph(self, df: pd.DataFrame) -> pd.DataFrame:
        concepts_list = await df2Graph(df, model='zephyr:latest')
        logger.info("Concepts list created %s", len(concepts_list))
        dfg1 = await graph2Df(concepts_list)

        dfg1.replace("", np.nan, inplace=True)
        dfg1.dropna(subset=["node_1", "node_2", 'edge'], inplace=True)
        dfg1 = dfg1[['node_1', 'node_2', 'edge', 'chunk_id', 'source']]
        
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


    def merge_relationships(self, df1: pd.DataFrame, df2:pd.DataFrame) -> pd.DataFrame:
        df = pd.concat([df1, df2], axis=0)
        df = (
            df.groupby(["node_1", "node_2", "source", "edge"])
            .agg({'count': 'sum'})
            .reset_index()
        )
        return df
    

    async def contruct_graph(self, df: pd.DataFrame) -> None:
        nodes = pd.concat([df['node_1'], df['node_2']], axis=0).unique()
        self.ingestion_repository.add_nodes(nodes)
        await self.ingestion_repository.add_edges(df)


    async def merge_nodes(self, similarity_threshold=0.8):
        await self.ingestion_repository.merge_nodes(similarity_threshold)


    def delete_all(self) -> None:
        self.ingestion_repository.delete_all()