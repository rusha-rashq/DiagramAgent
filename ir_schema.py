from typing import List

from pydantic import BaseModel


class Node(BaseModel):
    id: str
    label: str
    type: str


class Edge(BaseModel):
    source: str
    target: str


class DiagramIR(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
