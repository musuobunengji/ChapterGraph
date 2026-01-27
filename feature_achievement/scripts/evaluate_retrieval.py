import argparse
from collections import defaultdict
import numpy as np
from sqlmodel import Session, select

from feature_achievement.db.engine import engine
from feature_achievement.db.models import Edge


def summarize_scores(scores: list[float]) -> dict:
    if not scores:
        return {"count": 0}
    arr = np.array(scores)
    return {
        "count": len(scores),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "p90": float(np.percentile(arr, 90)),
        "p99": float(np.percentile(arr, 99)),
        "min": float(arr.min()),
        "max": float(arr.max()),
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate retrieval scores for a run")
    parser.add_argument("--run-id", type=int, required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    with Session(engine) as session:
        edges = session.exec(
            select(Edge).where(Edge.run_id == args.run_id)
        ).all()

    scores = [e.score for e in edges]
    print("Overall:", summarize_scores(scores))

    by_source = defaultdict(list)
    for e in edges:
        by_source[e.from_chapter].append(e.score)

    topk_scores = []
    for _, vals in by_source.items():
        vals.sort(reverse=True)
        topk_scores.extend(vals[: args.top_k])

    print(f"Top-{args.top_k} per source:", summarize_scores(topk_scores))


if __name__ == "__main__":
    main()
