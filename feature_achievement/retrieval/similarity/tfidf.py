from sklearn.metrics.pairwise import cosine_similarity
from .base import SimilarityScorer


class TfidfSimilarityScorer(SimilarityScorer):
    def __init__(self, tfidf_index):
        self.chapter_ids = tfidf_index["chapter_ids"]
        self.tfidf_matrix = tfidf_index["tfidf_matrix"]

    def score(self, src_id: str, tgt_id: str) -> float:
        i = self.chapter_ids.index(src_id)
        j = self.chapter_ids.index(tgt_id)

        return float(
            cosine_similarity(self.tfidf_matrix[i], self.tfidf_matrix[j])[0][0]
        )

    @property
    def name(self) -> str:
        return "tfidf"
