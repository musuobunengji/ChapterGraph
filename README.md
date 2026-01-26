# ChapterGraph

ChapterGraph builds a retrieval-backed knowledge graph across chapters from multiple technical books, persists it, and serves it via a FastAPI backend. A lightweight frontend renders the graph with D3 on canvas.

## Current status (as of Jan 2026)

- Backend: FastAPI + SQLModel
- Frontend: plain JS UI shell + graph-core in TypeScript (compiled with esbuild)
- Graph API: `/graph` returns book and chapter nodes plus weighted edges

## Key capabilities

- Ingestion and enrichment of book content into chapter-level signals
- Retrieval pipeline (candidate generation + TF-IDF similarity)
- Graph construction and persistence
- API for compute + query
- Canvas-based graph visualization (expand/collapse clusters)

## Project structure (high level)

```
feature_achievement/
  api/
    main.py
    routers/edges.py
  db/
    models.py
    crud.py
  retrieval/
    candidates/
    similarity/
    pipeline.py
  scripts/
    init_db.py

frontend/
  index.html
  app.js
  graph-core/
    buildView.ts
    reducer.ts
    types.ts
  graph-core-dist/   # compiled JS output
  package.json
```

## Backend: run

Start the API server (default port 8000):

```bash
uvicorn feature_achievement.api.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

If you need to initialize the DB schema (first time only):

```bash
python -m feature_achievement.scripts.init_db
```

## Frontend: build + run

The UI shell stays in JS. The graph-core is TypeScript and compiled with esbuild.

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

## API endpoints

- POST `/compute-edges`  
  Runs retrieval pipeline and persists nodes/edges for a new run.

- GET `/runs`  
  List runs (latest first).

- GET `/graph?run_id=...`  
  Returns graph nodes + edges for a run.

- GET `/edges?book_id=...`  
  Query edges for a given book.

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

## Notes

- The graph UI supports expand/collapse of book clusters (double-click).
- Chapter titles are provided by the backend (`/graph`) and shown in tooltips.
- If you edit `graph-core/*.ts`, re-run `npm run build:core`.
