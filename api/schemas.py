from pydantic import BaseModel
from typing import List, Dict, Any


class BookConfig(BaseModel):
    book_name: str
    content_path: str


class EdgeRequest(BaseModel):
    book_configs: List[BookConfig]


class Edge(BaseModel):
    from_id: str
    to_id: str
    type: str


class EdgeResponse(BaseModel):
    edge_count: int
    edges: List[Dict[str, Any]]
