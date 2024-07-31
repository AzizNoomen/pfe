from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from app.repositories.retrieval_repository import RetrievalRepository
from app.helpers.df_helpers import query2Dataframe, query2Graph, graph2Df
from sentence_transformers import CrossEncoder
from configuration.logging import logger
import httpx


class RetrievalService:
    def __init__(self, retrieval_repository: RetrievalRepository):
        self.retrieval_repository = retrieval_repository
    
    def cross_encoder_rerank(self, question:str, df: pd.DataFrame, top_k:int, reranker:str ="ms-marco-MiniLM-L-6-v2") -> pd.DataFrame:
        logger.info("dataframe content", df)
        cross_encoder = CrossEncoder(f'cross-encoder/{reranker}')
        # Ensure the dataframe is not empty and has the required columns
        if df.empty or 'relationship' not in df.columns:
            logger.info("DataFrame is empty or does not contain the required 'relationship' column.")
            return pd.DataFrame()  # Return an empty DataFrame

        # Create pairs of query and text from dataframe
        pairs = [[question, row['relationship']] for _, row in df.iterrows()]

        # Check if pairs list is empty
        if not pairs:
            logger.info("No valid pairs to rerank.")
            return pd.DataFrame()  # Return an empty DataFrame

        # Predict scores using cross encoder
        try:
            logger.info("Predicting scores using cross encoder...")
            scores = cross_encoder.predict(pairs)
            logger.info("Cross encoder prediction completed successfully.")
        except Exception as e:
            logger.info(f"Error during cross encoder prediction: {e}")

        # Add scores to dataframe and sort
        df['cross_encoder_score'] = scores
        df_sorted = df.sort_values(by='cross_encoder_score', ascending=False)

        return df_sorted.head(top_k)
    

    async def handle_question(self, question: str, model: str = "zephyr:latest") -> pd.DataFrame:
        df_question = query2Dataframe(question)
        question_concepts_list = await query2Graph(df_question, model=model)

        if question_concepts_list:
            dfg_question = await graph2Df(question_concepts_list)
            dfg_question.replace("", np.nan, inplace=True)
            dfg_question.dropna(subset=["node_1", "node_2", 'edge'], inplace=True)
            return dfg_question
        
        else:
            df = pd.DataFrame([{"edge": question}])
            return df


    async def retrieve(self, question: str, model: str = "zephyr:latest", top_n: int = 10, similarity_threshold: float = 0.5, reranker:str = None) -> pd.DataFrame:
        
        dfg_question = await self.handle_question(question, model)

        if ('node_1' and 'node_2') in dfg_question.columns:
            keyword_results = self.retrieval_repository.keyword_search(dfg_question)
        
        else:
            keyword_results = pd.DataFrame()
        
        semantic_results = await self.retrieval_repository.semantic_search(dfg_question, top_n=top_n + 5, similarity_threshold=similarity_threshold)
        combined_results = pd.concat([keyword_results, semantic_results], ignore_index=True)
        logger.info("dataframe content", combined_results)
        combined_results.dropna(inplace=True)

        if reranker:
            logger.info("retrieval with reranker")
            reranked_results = self.cross_encoder_rerank(question, combined_results, top_n, reranker)
            return reranked_results
        
        return combined_results
    

    def get_all(self) -> pd.DataFrame:
        return self.retrieval_repository.get_all()


    def get_graph(self) -> JSONResponse:
        return self.retrieval_repository.get_graph()
