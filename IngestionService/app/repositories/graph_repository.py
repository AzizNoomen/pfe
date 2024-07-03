import httpx
import pandas as pd
import logging
from typing import List
from app.database import db
from app.exceptions.graph_exceptions import DatabaseNotInitialized, ModelServiceUnavailable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphRepository:
    def __init__(self):
        self.db = db

    
    def add_nodes(self, nodes: List[str]) -> None:
        if not self.db:
            raise DatabaseNotInitialized()
        
        logger.info('adding nodes to neo4j graph')
        
        with self.db.driver.session() as session:
            for node in nodes:
                session.run(
                    "MERGE (:Node {name: $name})",
                    {"name": node}
                )
        logger.info('nodes added successfully')


    async def add_edges(self, dfg: pd.DataFrame) -> None:
        if not self.db:
            raise DatabaseNotInitialized()

        logger.info('adding egdes to neo4j graph')
        with self.db.driver.session() as session:
            for _, row in dfg.iterrows():
                # Assuming you have a model for generating embeddings
                if row['edge'] != 'contextual proximity':
                    try:
                        async with httpx.AsyncClient(timeout=2000) as client:
                            response = await client.post(f"http://model-service:8000/api/ollama/encode", json={"model": "all-minilm", "prompt": row['edge']})
                            response.raise_for_status()
                            embedding = response.json()
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


    def delete_all(self) -> None:
        if not self.db:
            raise DatabaseNotInitialized()
        
        with self.db.driver.session() as session:
            session.run(
                "MATCH (n) DETACH DELETE n"
            )

    

