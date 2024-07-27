import httpx
import pandas as pd
import Levenshtein
from typing import List
from app.exceptions.service_exceptions import ModelServiceUnavailable
from sklearn.metrics.pairwise import cosine_similarity
from app.helpers.db_helpers import DBHelper
from configuration.logging import logger


class IngestionRepository:

    def __init__(self, database_helper: DBHelper):
        self.database_helper = database_helper

    def add_nodes(self, nodes: List[str]) -> None:
        logger.info('adding nodes to neo4j graph')
        
        with self.database_helper.session() as session:
            for node in nodes:
                session.run(
                    "MERGE (:Node {name: $name})",
                    {"name": node}
                )
        logger.info('nodes added successfully')


    async def add_edges(self, dfg: pd.DataFrame) -> None:

        logger.info('adding edges to neo4j graph')
        with self.database_helper.session() as session:
            for _, row in dfg.iterrows():
                # Assuming you have a model for generating embeddings
                if row['edge'] != 'contextual proximity':
                    try:
                        async with httpx.AsyncClient(timeout=2000) as client:
                            response = await client.post(f"http://model-service:8000/api/ollama/encode", json={"model_name": "all-minilm:latest", "prompt": row['edge']})
                            response.raise_for_status()
                            embedding = response.json()['embedding']
                            logger.info("\nembeddings: %s", embedding)
                    except httpx.HTTPStatusError:
                        raise ModelServiceUnavailable()
                else:
                    embedding = None
                
                if embedding is not None:
                    session.run(
                        "MATCH (a:Node {name: $node1}), (b:Node {name: $node2}) "
                        "MERGE (a)-[r:RELATIONSHIP {title: $title, source: $source, weight: $weight}]-(b) "
                        "WITH r "
                        "CALL db.create.setRelationshipVectorProperty(r, 'embedding', $embedding) "
                        "RETURN r",
                        {
                            "node1": row["node_1"],
                            "node2": row["node_2"],
                            "title": row["edge"],
                            "embedding": embedding,
                            "weight": row["count"],
                            "source": row["source"]
                        },
                    )
                else:
                    session.run(
                        "MATCH (a:Node {name: $node1}), (b:Node {name: $node2}) "
                        "MERGE (a)-[r:contextual_proximity {weight: $weight, source: $source}]-(b) "
                        "RETURN r",
                        {
                            "node1": row["node_1"],
                            "node2": row["node_2"],
                            "weight": row["count"],
                            "source": row["source"],
                        },
                    )
        logger.info('edges added successfully')


    async def merge_nodes(self, similarity_threshold:float = 0.8) -> None:
        nodes = []
        embeddings = []

        with self.database_helper.session() as session:
            result = session.run("MATCH (n:Node) RETURN n.name AS name")
            for record in result:
                node_name = record["name"]
                nodes.append(node_name)

                try:
                    async with httpx.AsyncClient(timeout=2000) as client:
                        response = await client.post(f"http://model-service:8000/api/ollama/encode", json={"model_name": "all-minilm:latest", "prompt": node_name})
                        response.raise_for_status()
                        embedding = response.json()['embedding']
                        embeddings.append(embedding)

                except httpx.HTTPStatusError:
                    raise ModelServiceUnavailable()

        similarities = cosine_similarity(embeddings)
        similar_pairs = []
        weight_cosine=0.5
        weight_levenshtein=0.5

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                cosine_sim = similarities[i, j]
                levenshtein_dist = Levenshtein.distance(nodes[i], nodes[j]) / max(len(nodes[i]), len(nodes[j]))
                combined_similarity = weight_cosine * cosine_sim + weight_levenshtein * (1 - levenshtein_dist)
                if combined_similarity >= similarity_threshold:
                    similar_pairs.append((nodes[i], nodes[j], combined_similarity))
        

        with self.database_helper.session() as session:
            for node1, node2, similarity in similar_pairs:
                logger.info(f"Merging nodes: {node1} and {node2} with similarity {similarity}")
                session.run("""
                    MATCH (n1:Node {name: $node1}), (n2:Node {name: $node2})
                    WHERE id(n1) <> id(n2)
                    CALL apoc.refactor.mergeNodes([n1, n2]) YIELD node
                    SET node.name = CASE
                        WHEN size($node1) >= size($node2) THEN $node1
                        ELSE $node2
                    END
                    RETURN node
                """, {"node1": node1, "node2": node2})

    
    def delete_all(self) -> None:

        with self.database_helper.session() as session:
            session.run(
                "MATCH (n) DETACH DELETE n"
            )

    

