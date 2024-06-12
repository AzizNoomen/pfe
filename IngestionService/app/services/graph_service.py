from app.repositories.graph_repository import GraphRepository
from typing import List
from app.models.graph_models import Node, Edge
from pathlib import Path
from fastapi import UploadFile

class GraphService:
    def __init__(self):
        self.graph_repository = GraphRepository()

    def create_graph(self, nodes: List[Node], edges: List[Edge]):
        self.graph_repository.add_nodes(nodes)
        self.graph_repository.add_edges(edges)
    

    async def create_graph_from_files(self, uploaded_files: List[UploadFile], output_directory: Path):
        await self.graph_repository.load_documents_and_create_graph(uploaded_files, output_directory)