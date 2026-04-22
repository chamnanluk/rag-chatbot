# RAG Chatbot (OpenAI + LangChain + ChromaDB + Docker)

A practical Retrieval-Augmented Generation chatbot that indexes your own documents and answers questions with grounded context.

## Quick Start

1. Create environment and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure env:
   ```bash
   cp .env.example .env
   # then set OPENAI_API_KEY in .env
   ```
3. Add documents to `data/raw/` (`.txt`, `.md`, `.pdf`).
4. Build index:
   ```bash
   python scripts/ingest_docs.py
   ```
5. Run API:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
6. Test endpoint:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"question":"Summarize the key policies"}'
   ```

## Project Structure

```text
app/
  api/            # FastAPI routes + request/response schemas
  chains/         # prompt builder + RAG chain orchestration
  core/           # config, logging, app exceptions
  ingest/         # document loading and chunking pipeline
  retrieval/      # embeddings, Chroma vectorstore, retriever
  services/       # chat and citation business logic
  utils/          # small helper functions
scripts/          # ingest, rebuild index, smoke-test scripts
prompts/          # system + user prompt templates
data/             # raw files + persisted Chroma index
docker/           # Dockerfile and entrypoint
tests/            # MVP tests
```

## RAG Flow

1. Load docs from `data/raw`
2. Split into chunks
3. Embed chunks with OpenAI embeddings
4. Persist vectors in ChromaDB
5. Embed query, retrieve top-k chunks
6. Build prompt with retrieved context
7. Generate grounded answer using OpenAI chat model

## Docker

```bash
docker compose up --build
```

API will be available at `http://localhost:8000`.

## Useful Commands

- Ingest docs: `python scripts/ingest_docs.py`
- Rebuild index: `python scripts/rebuild_index.py`
- Smoke chat: `python scripts/smoke_test_chat.py`
- Run tests: `pytest -q`
