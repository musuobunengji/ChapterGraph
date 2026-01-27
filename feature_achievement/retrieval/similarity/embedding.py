import numpy as np
from .base import SimilarityScorer


class EmbeddingSimilarityScorer(SimilarityScorer):
    def __init__(self, embedding_index: dict):
        self.chapter_ids = embedding_index["chapter_ids"]
        self.embeddings = embedding_index["embeddings"]
        self.id_to_idx = {cid: i for i, cid in enumerate(self.chapter_ids)}
        self.model_name = embedding_index.get("model_name", "embedding")

    def score(self, src_id: str, tgt_id: str) -> float:
        i = self.id_to_idx.get(src_id)
        j = self.id_to_idx.get(tgt_id)
        if i is None or j is None:
            return 0.0
        return float(np.dot(self.embeddings[i], self.embeddings[j]))

    @property
    def name(self) -> str:
        return "embedding"
