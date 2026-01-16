from abc import ABC, abstractmethod


class SimilarityScorer(ABC):
    @abstractmethod
    def score(self, src_id: str, tgt_id: str) -> float:
        pass

    @property
    def name(self) -> str:
        raise NotImplementedError
