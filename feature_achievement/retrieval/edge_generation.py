def generate_edges(enriched_books, retrieval_pipeline):
    edges = []

    for book in enriched_books:
        for chapter in book["chapters"]:
            src_id = chapter["id"]
            edges.extend(retrieval_pipeline.retrieve(src_id))

    return edges
