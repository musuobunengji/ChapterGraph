"""
edge generation
    candidate pair (A, B)
        → similarity(A, B) -> score
        → filtering (threshold / top-k)
            score -> keep or discard (threshold)
            scores -> choose strongest (top-k)

"""


def generate_edges(enriched_books, keyword_index):
    edges = []

    chapter_signals = build_chapter_signal_map(enriched_books)

    for book in enriched_books:
        for chapter in book["chapters"]:
            src_id = chapter["id"]
            keywords = (
                chapter.get("signals", {}).get("features", {}).get("keywords", [])
            )

            candidates = set()
            for kw in keywords:
                candidates |= keyword_index.get(kw, set())

            candidates.discard(src_id)

            signal_A = chapter_signals[src_id]

            src_book = get_book_id(src_id)
            for tgt_id in candidates:
                tgt_book = get_book_id(tgt_id)
                if src_book == tgt_book:
                    continue
                signal_B = chapter_signals[tgt_id]
                score = rule_based_similarity(signal_A, signal_B)
                edges.append(
                    {
                        "from": src_id,
                        "to": tgt_id,
                        "type": "keyword_overlap",
                        "score": score,
                    }
                )

    return edges


def compute_similarity(signal_A: dict, signal_B: dict) -> float:
    """
    Compute semantic similarity between two chapter signals.
    """
    raise NotImplementedError


def rule_based_similarity(signal_A: dict, signal_B: dict) -> float:
    keywords_A = set(signal_A.get("features", {}).get("keywords", []))
    keywords_B = set(signal_B.get("features", {}).get("keywords", []))

    if not keywords_A or not keywords_B:
        return 0.0

    return float(len(keywords_A & keywords_B))


def build_chapter_signal_map(enriched_books):
    """chapter_id -> signals"""
    chapter_signals = {}

    for book in enriched_books:
        for chapter in book["chapters"]:
            chapter_id = chapter["id"]
            signals = chapter.get("signals", {})
            chapter_signals[chapter_id] = signals

    return chapter_signals


def get_book_id(chapter_id: str) -> str:
    """spring-in-action::ch1->{book_id}::{chapter_id}"""
    return chapter_id.split("::")[0]
