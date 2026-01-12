from abc import ABC, abstractmethod


class CandidateGenerator(ABC):
    @abstractmethod
    def generate(self, src_id: str) -> set[str]:
        pass
