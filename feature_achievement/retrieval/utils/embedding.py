import numpy as np
from sentence_transformers import SentenceTransformer


def build_embedding_index(chapter_texts: dict, model_name: str = "all-MiniLM-L6-v2"):
    """
    Input:
        chapter_texts: dict[chapter_id] -> text
    Output:
        {
            "chapter_ids": [...],
            "embeddings": np.ndarray,
            "model_name": str
        }
    """
    chapter_ids = list(chapter_texts.keys())
    corpus = [chapter_texts[cid] or "" for cid in chapter_ids]

    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        corpus,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    return {
        "chapter_ids": chapter_ids,
        "embeddings": np.asarray(embeddings),
        "model_name": model_name,
    }
