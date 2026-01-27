# ChapterGraph

ChapterGraph builds a retrieval-backed knowledge graph across chapters from multiple technical books, persists it in PostgreSQL, and serves it via a FastAPI backend. A lightweight frontend renders the graph on a canvas with D3, supporting expand/collapse of book clusters.

---

## Current status (Jan 2026)

- Backend: FastAPI + SQLModel + PostgreSQL
- Retrieval: TF‑IDF similarity (default) + optional sentence‑transformers embeddings
- Frontend: JS UI shell + TypeScript graph‑core (compiled with esbuild)
- Graph API: `/graph` returns book + chapter nodes with weighted edges

---

## Project structure (high level)

```
feature_achievement/
  api/
    main.py
    routers/edges.py
    routers/compute_edges_request.py
  db/
    engine.py
    models.py
    crud.py
  retrieval/
    candidates/
    similarity/
      tfidf.py
      embedding.py
    utils/
      tfidf.py
      embedding.py
    pipeline.py
  scripts/
    init_db.py
    evaluate_retrieval.py

frontend/
  index.html
  app.js
  graph-core/
    buildView.ts
    reducer.ts
    types.ts
  graph-core-dist/
  package.json

scripts/
  run_local.ps1
```

---

## Backend: run

Start the API server (default port 8000):

```bash
uvicorn feature_achievement.api.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

Initialize DB schema (first time only):

```bash
python -m feature_achievement.scripts.init_db
```

---

## Frontend: build + run

The UI shell stays in JS. The graph‑core is TypeScript and compiled with esbuild.

```bash
cd frontend
npm i -D esbuild
npm run build:core
python -m http.server 5500
```

Open:

```
http://127.0.0.1:5500/index.html
```

Optional API base override:

```
http://127.0.0.1:5500/index.html?api=http://127.0.0.1:8000
```

---

## API endpoints

- POST `/compute-edges`  
  Runs the retrieval pipeline and persists nodes/edges for a new run.

- GET `/runs`  
  List runs (latest first).

- GET `/graph?run_id=...`  
  Returns graph nodes + edges for a run.

- GET `/edges?book_id=...`  
  Query edges for a given book.

---

## Graph response shape (simplified)

```json
{
  "nodes": [
    { "id": "book-id", "type": "book", "size": 18 },
    { "id": "book-id::ch1", "type": "chapter", "book_id": "book-id", "title": "Intro" }
  ],
  "edges": [
    { "source": "book-id::ch1", "target": "other::ch2", "score": 0.42, "type": "tfidf" }
  ]
}
```

---

## Embedding scorer (optional)

Install sentence‑transformers:

```bash
pip install sentence-transformers
```

Use embedding similarity in `/compute-edges`:

```json
{
  "book_ids": ["spring-in-action", "spring-start-here", "springboot-in-action"],
  "candidate_generator": "tfidf_token",
  "similarity": "embedding",
  "embedding_model": "all-MiniLM-L6-v2",
  "min_score": 0.1
}
```

---

## Retrieval evaluation (score statistics)

This script summarizes score distribution (overall + top‑k per source). It is **not** a ground‑truth hit‑rate metric.

```bash
python -m feature_achievement.scripts.evaluate_retrieval --run-id 3 --top-k 5
```

---

## One‑click local run (PowerShell)

```powershell
.\scripts\run_local.ps1
```

---

## Notes

- Double‑click a book node to expand/collapse its chapters.
- Chapter titles come from `/graph` and are shown in tooltips.
- If you edit `graph-core/*.ts`, re‑run `npm run build:core`.
