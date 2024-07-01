import logging
import pandas as pd
import numpy as np
from app.repositories.retrieval_repository import RetrievalRepository
from app.helpers.df_helpers import query2Dataframe, query2Graph, graph2Df


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(self):
        self.retrieval_repository = RetrievalRepository()
    
    async def retrieve(self, question: str, model: str = "zephyr:latest", top_n: int = 10, similarity_threshold: float = 0.5) -> pd.DataFrame:
        df_question = query2Dataframe(question)
        question_concepts_list = await query2Graph(df_question, model=model)

        logger.info("question concepts")

        dfg_question = await graph2Df(question_concepts_list)

        dfg_question.replace("", np.nan, inplace=True)
        dfg_question.dropna(subset=["node_1", "node_2", 'edge'], inplace=True)

        keyword_results = self.retrieval_repository.keyword_search(dfg_question)
        semantic_results = await self.retrieval_repository.semantic_search(dfg_question, top_n=top_n, similarity_threshold=similarity_threshold)
        combined_results = pd.concat([keyword_results, semantic_results], ignore_index=True)

        logger.info("combined results", combined_results)
        
        return combined_results

    def close(self):
        self.retrieval_repository.close()