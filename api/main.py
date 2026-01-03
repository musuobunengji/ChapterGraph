from fastapi import FastAPI
from api.schemas import EdgeRequest, EdgeResponse

from book_content.feature_achievement import (
    load_all_enriched_data_from_configs,
    build_keyword_index,
    generate_edges,
)

app = FastAPI()


@app.post("/edges/preview", response_model=EdgeResponse)
def generate_edges_preview(req: EdgeRequest):
    enriched_books = load_all_enriched_data_from_configs(
        [cfg.model_dump() for cfg in req.book_configs]
    )
    keyword_index = build_keyword_index(enriched_books)
    edges = generate_edges(enriched_books, keyword_index)

    return EdgeResponse(edge_count=len(edges), edges=edges)
