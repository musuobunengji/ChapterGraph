from sklearn.metrics.pairwise import cosine_similarity


def print_top_k_similar_chapters(
    src_id: str, tfidf_index: dict, enriched_books: list, k: int = 5
):
    chapter_ids = tfidf_index["chapter_ids"]
    tfidf_matrix = tfidf_index["tfidf_matrix"]

    if src_id not in chapter_ids:
        raise ValueError(f"Chapter id not found:{src_id}")

    src_idx = chapter_ids.index(src_id)
    src_vec = tfidf_matrix[src_idx]

    sims = cosine_similarity(src_vec, tfidf_matrix)[0]

    scored = [
        (chapter_ids[i], float(sims[i]))
        for i in range(len(chapter_ids))
        if chapter_ids[i] != src_id
    ]

    scored.sort(key=lambda x: x[1], reverse=True)

    chapter_map = {
        chapter["id"]: chapter
        for book in enriched_books
        for chapter in book["chapters"]
    }

    print(f"\n=== Top {k} TF-IDF similar chapters for ===")
    print(f"SOURCE: {src_id}\n")

    for rank, (cid, score) in enumerate(scored[:k], start=1):
        ch = chapter_map.get(cid)
        title = ch.get("title", "(no title)") if ch else "(missing)"
        book_id = cid.split("::")[0]

        print(f"[{rank}] {cid}")
        print(f"    book   : {book_id}")
        print(f"    title  : {title}")
        print(f"    score  : {score:.4f}")
        print()
