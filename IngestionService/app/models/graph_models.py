from dataclasses import dataclass
import uuid

@dataclass
class Node:
    name: str

    def __init__(self, name: str):
        self.name = name

@dataclass
class Edge:
    node1: Node
    node2: Node
    relationship: str

    def __init__(self, node1: Node, node2: Node, edge: str):
        self.node1 = node1
        self.node2 = node2
        self.relationship = edge