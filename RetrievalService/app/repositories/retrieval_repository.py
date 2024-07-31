import httpx
import pandas as pd
from app.exceptions.service_exceptions import ModelServiceUnavailable
from app.helpers.db_helpers import DBHelper
from configuration.logging import logger
from fastapi.responses import JSONResponse


class RetrievalRepository:
    def __init__(self, database_helper: DBHelper):
        self.database_helper = database_helper
    
    def keyword_search(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("key word search started")

        nodes = pd.concat([df['node_1'], df['node_2']]).drop_duplicates().tolist()

        query = """
        MATCH (n:Node)
        WHERE any(keyword IN $keywords WHERE n.name CONTAINS keyword)
        WITH COLLECT(DISTINCT n.name) AS nodes
        UNWIND nodes AS node1
        UNWIND nodes AS node2
        WITH node1, node2 WHERE node1 < node2
        OPTIONAL MATCH (n1:Node {name: node1})-[r:RELATIONSHIP]-(n2:Node {name: node2})
        WITH node1 AS node_1, r.title AS relationship, node2 AS node_2
        WHERE relationship IS NOT NULL
        RETURN node_1, relationship, node_2
        """
        
        with self.database_helper.session() as session:
            result = session.run(query, {'keywords': nodes})
            relationships = [(record['node_1'], record['relationship'], record['node_2']) for record in result]

        df_results = pd.DataFrame(relationships, columns=['node_1', 'relationship', 'node_2'])
        df_results['score'] = 1
        df_results['context'] = [[] for _ in range(len(df_results))]

        logger.info('keyword search done')

        return df_results


    async def semantic_search(self, df: pd.DataFrame, top_n: int = 10, similarity_threshold: float = 0.5) -> pd.DataFrame:
        edges = df['edge'].tolist()
        embeddings = []

        logger.info("semantic search started")

        for e in edges:
            try:
                async with httpx.AsyncClient(timeout=2000) as client:
                    response = await client.post(f"http://model-service:8000/api/ollama/encode", json={"model_name": "all-minilm:latest", "prompt": e})
                    response.raise_for_status()
                    embedding = response.json()['embedding']
                    embeddings.append(embedding)
                    
            except httpx.HTTPStatusError:
                raise ModelServiceUnavailable()

        query = """
        UNWIND $edge_embeddings AS edge_embedding
        MATCH (a)-[r:RELATIONSHIP]->(b)
        WHERE r.embedding IS NOT NULL
        WITH edge_embedding, r, a, b, gds.similarity.cosine(edge_embedding, r.embedding) AS score
        WHERE score >= $similarity_threshold
        OPTIONAL MATCH (a)-[:contextual_proximity]-(c)
        OPTIONAL MATCH (b)-[:contextual_proximity]-(d)
        WITH a.name AS node_source, r.title AS text, score, b.name AS node_target, COLLECT(DISTINCT c.name) + COLLECT(DISTINCT d.name) AS context
        ORDER BY score DESC
        LIMIT $top_n
        RETURN node_source, text, score, node_target, context
        """

        with self.database_helper.session() as session:
            result = session.run(query, {'edge_embeddings': embeddings, 'similarity_threshold': similarity_threshold, 'top_n': top_n})
            records = [r for r in result]

        records_with_unique_context = []
        for record in records:
            context_set = set(record['context'])
            new_record = {
                'node_1': record['node_source'],
                'relationship': record['text'],
                'node_2': record['node_target'],
                'score': record['score'],
                'context': list(context_set)
            }
            records_with_unique_context.append(new_record)

        df_results = pd.DataFrame(records_with_unique_context)
        logger.info("semantic search done")
        return df_results

    def get_all(self) -> pd.DataFrame:
        
        query = """
        MATCH (n)-[r]->(m)
        RETURN n.name AS node_source, r.title AS text, m.name AS node_target
        """

        with self.database_helper.session() as session:
            result = session.run(query)
            records = [r for r in result]
        
        records_with_unique_context = []
        for record in records:
            if record['text']:
                new_record = {
                    'node_1': record['node_source'],
                    'relationship': record['text'],
                    'node_2': record['node_target']
                }
            else:
                new_record = {
                    'node_1': record['node_source'],
                    'relationship': "contextual proximity",
                    'node_2': record['node_target']
                }
            records_with_unique_context.append(new_record)

        df_results = pd.DataFrame(records_with_unique_context)
        return df_results
    
    def get_graph(self) -> JSONResponse:
        df = self.get_all()
        nodes = []
        node_ids = set()
        edges = []

        for _, row in df.iterrows():
            # Add node 1 if not already in the list
            if row['node_1'] not in node_ids:
                nodes.append({"data": {"id": row['node_1'], "label": row['node_1']}})
                node_ids.add(row['node_1'])
            
            # Add node 2 if not already in the list
            if row['node_2'] not in node_ids:
                nodes.append({"data": {"id": row['node_2'], "label": row['node_2']}})
                node_ids.add(row['node_2'])
            
            # Add edge
            edges.append({"data": {"source": row['node_1'], "target": row['node_2'], "label": row['relationship']}})

        graph_data = {
            "nodes": nodes,
            "edges": edges
        }

        return JSONResponse(content=graph_data)

    