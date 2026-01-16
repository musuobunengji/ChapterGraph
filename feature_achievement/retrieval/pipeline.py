class RetrievalPipeline:
    def __init__(
        self,
        candidate_generator,
        similarity_scorer,
        min_score: float = 0.1,
    ):
        self.candidate_generator = candidate_generator
        self.similarity_scorer = similarity_scorer
        self.min_score = min_score

    @staticmethod
    def get_book_id(chapter_id: str) -> str:
        """spring-in-action::ch1->{book_id}::{chapter_id}"""
        return chapter_id.split("::")[0]

    def retrieve(self, src_id: str) -> list[dict]:
        edges = []
        src_book = self.get_book_id(src_id)
        candidates = self.candidate_generator.generate(src_id)

        for tgt_id in candidates:
            tgt_book = self.get_book_id(tgt_id)
            if src_book == tgt_book:
                continue

            score = self.similarity_scorer.score(src_id, tgt_id)
            if score < self.min_score:
                continue

            edges.append(
                {
                    "from": src_id,
                    "to": tgt_id,
                    "score": score,
                    "type":self.similarity_scorer.name,
                }
            )

        return edges
