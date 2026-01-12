from collections import defaultdict
from .base import CandidateGenerator


class TfidfTokenCandidateGenerator(CandidateGenerator):
    def __init__(self, chapter_top_tokens, token_index, min_shared_tokens=2):
        self.chapter_top_tokens = chapter_top_tokens
        self.token_index = token_index
        self.min_shared_tokens = min_shared_tokens

    def generate(self, src_id: str) -> set[str]:
        overlap = defaultdict(int)

        for token in self.chapter_top_tokens.get(src_id, []):
            for tgt_id in self.token_index.get(token, []):
                if tgt_id != src_id:
                    overlap[tgt_id] += 1

        return {
            tgt_id for tgt_id, cnt in overlap.items() if cnt >= self.min_shared_tokens
        }
