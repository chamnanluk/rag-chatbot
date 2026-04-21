# RAG Chatbot Project Blueprint (OpenAI + LangChain + ChromaDB + Docker)

This repository now contains a **portfolio-ready blueprint** for building a practical Retrieval-Augmented Generation (RAG) chatbot using your own data.

---

## 1) Project Overview

### What this project does
You will build a chatbot that answers questions based on your own documents (PDFs, Markdown, text, policies, notes, etc.) instead of only relying on general model knowledge.

### Main components and purpose
- **OpenAI API**: Generates natural-language answers and (optionally) embeddings.
- **LangChain**: Orchestrates the RAG pipeline (loading docs, chunking, retrieval, prompting, chain execution).
- **ChromaDB**: Stores vector embeddings and metadata so relevant chunks can be searched fast.
- **Docker**: Packages app + dependencies into a repeatable runtime for local dev and deployment.

### How they work together
1. Documents are loaded and split into chunks.
2. Chunks become vectors via embeddings.
3. Vectors are stored in ChromaDB.
4. User asks a question.
5. Retriever pulls most relevant chunks.
6. Prompt template combines question + retrieved context.
7. OpenAI model returns grounded answer.

---

## 2) System Architecture

### End-to-end RAG workflow (text diagram)

```text
[Raw Docs] 
   -> [Document Loaders]
   -> [Chunker / Text Splitter]
   -> [Embedding Model]
   -> [ChromaDB Vector Store]

[User Query]
   -> [Query Embedding]
   -> [Retriever (top-k chunks)]
   -> [Prompt Builder]
   -> [OpenAI Chat Model]
   -> [Answer + Sources]
```

### Step-by-step data flow
1. **Document loading**
   - Read files from `data/raw/` using LangChain loaders.
2. **Text chunking**
   - Split long text into overlap-aware chunks (e.g., 800 chars with 120 overlap).
3. **Embeddings creation**
   - Convert each chunk into numeric vectors.
4. **Vector storage**
   - Save vectors + metadata (`source`, `page`, `section`, `doc_type`) in Chroma.
5. **Retrieval**
   - User query is embedded and similarity-searched against Chroma.
6. **Prompt construction**
   - Compose system instructions + retrieved context + user query.
7. **LLM response generation**
   - Chat model produces final answer (optionally with citations/snippets).

---

## 3) Recommended Project Folder Structure

```text
rag-chatbot/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes_chat.py
│   │   └── schemas.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── exceptions.py
│   ├── ingest/
│   │   ├── loaders.py
│   │   ├── chunker.py
│   │   └── pipeline.py
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   ├── retriever.py
│   │   └── reranker.py   # optional later
│   ├── chains/
│   │   ├── prompt_builder.py
│   │   └── rag_chain.py
│   ├── services/
│   │   ├── chat_service.py
│   │   └── citation_service.py
│   └── utils/
│       ├── file_utils.py
│       └── token_utils.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── chroma/
├── prompts/
│   ├── system_prompt.txt
│   └── answer_template.txt
├── scripts/
│   ├── ingest_docs.py
│   ├── rebuild_index.py
│   └── smoke_test_chat.py
├── tests/
│   ├── test_chunker.py
│   ├── test_retriever.py
│   └── test_chat_api.py
├── docker/
│   ├── Dockerfile
│   └── entrypoint.sh
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── README.md
└── Makefile
```

### Folder/file purpose and why it matters
- `app/main.py`: app bootstrap (FastAPI/CLI), dependency wiring.
- `app/core/config.py`: central settings (API keys, model names, chunk params).
- `app/ingest/*`: deterministic ingestion logic.
- `app/retrieval/*`: retrieval mechanics and vector DB integration.
- `app/chains/*`: prompt + chain assembly to keep LLM logic isolated.
- `app/services/*`: application business logic independent from transport layer.
- `data/raw`: source documents; `data/chroma`: persisted vector DB.
- `prompts/`: editable prompts outside code (clean experimentation).
- `scripts/`: operational tasks (ingest/reindex/smoke tests).
- `tests/`: guardrails for chunking/retrieval/API behavior.
- `docker/` + compose: reproducible local and deployment runtime.

---

## 4) Development Roadmap

### Phase 1 — Environment setup
- **Objective**: runnable skeleton.
- **Tasks**: create venv, dependencies, `.env`, basic app entry.
- **Expected output**: app starts and prints health check.
- **Common mistakes**: hardcoding keys, no `.env.example`, no version pinning.

### Phase 2 — Document ingestion
- **Objective**: load your data reliably.
- **Tasks**: implement loaders for txt/md/pdf, normalize metadata.
- **Expected output**: parsed `Document` objects.
- **Common mistakes**: mixing unsupported encodings, losing source metadata.

### Phase 3 — Embeddings + Chroma storage
- **Objective**: build searchable vector index.
- **Tasks**: chunk text, embed chunks, persist to Chroma.
- **Expected output**: `data/chroma/` populated.
- **Common mistakes**: too-large chunks, no overlap, no persistence path.

### Phase 4 — Retrieval pipeline
- **Objective**: return relevant context.
- **Tasks**: configure retriever (`k`, score threshold), metadata filters.
- **Expected output**: top-k chunks returned for test queries.
- **Common mistakes**: retrieving too many chunks and blowing token budget.

### Phase 5 — Chatbot interaction
- **Objective**: full RAG question-answer flow.
- **Tasks**: prompt template, combine context, call chat model, return answer + sources.
- **Expected output**: working CLI/API endpoint.
- **Common mistakes**: prompt too vague, not instructing model to say “I don’t know.”

### Phase 6 — Docker deployment
- **Objective**: reproducible execution environment.
- **Tasks**: Dockerfile, compose, mount data volume, env injection.
- **Expected output**: `docker compose up` runs app end-to-end.
- **Common mistakes**: forgetting persistent volume for Chroma.

### Phase 7 — Production hardening
- **Objective**: portfolio-grade quality.
- **Tasks**: logging, retries, tests, basic eval set, observability.
- **Expected output**: stable baseline with measurable quality.
- **Common mistakes**: no evaluation before adding features.

---

## 5) Core Files to Build First (MVP)

1. `app/core/config.py`
   - load env vars and typed settings.
2. `app/ingest/pipeline.py`
   - read docs, split chunks, return clean records.
3. `app/retrieval/vectorstore.py`
   - create/load Chroma collection; add/query embeddings.
4. `app/chains/rag_chain.py`
   - retrieval + prompt + generation orchestration.
5. `scripts/ingest_docs.py`
   - one command to ingest and index local files.
6. `app/main.py`
   - minimal API/CLI entry for chatting.

### Suggested build order
`config -> loaders/chunker -> vectorstore -> rag_chain -> ingest script -> API/CLI`

---

## 6) Recommended Tech Decisions (Beginner-friendly + practical)

### OpenAI model usage
- Start with **`gpt-4.1-mini`** (good quality/price for app prototyping).
- Keep model name configurable via env.

### Embedding model
- Use **`text-embedding-3-small`** for first version (cost-efficient, strong baseline).

### LangChain components
- `DocumentLoaders` for file parsing.
- `RecursiveCharacterTextSplitter` for chunking.
- `Chroma` vector store integration.
- `as_retriever(search_type="similarity", search_kwargs={"k": 4})`.
- `RunnableSequence` or LCEL pipeline for clean composition.

### ChromaDB setup
- Use **persistent local storage** first: `data/chroma`.
- One collection per project domain.
- Store metadata now; it enables filtering later.

### Config management
- Use `pydantic-settings` in `config.py`.
- Add `.env.example` and never commit real secrets.

### Environment variables (minimum)
- `OPENAI_API_KEY`
- `OPENAI_CHAT_MODEL`
- `OPENAI_EMBEDDING_MODEL`
- `CHROMA_PERSIST_DIR`
- `TOP_K`
- `LOG_LEVEL`

### Logging
- Structured logs with `logging` + JSON format for API mode.
- Log ingest counts, chunk counts, retrieval scores, request IDs.

### Error handling
- Validate config at startup.
- Retry transient OpenAI errors.
- Return safe fallback on empty retrieval (“I couldn’t find enough context in your docs.”).

---

## 7) Docker Setup Plan

### Required files
- `docker/Dockerfile`
  - builds Python runtime, installs dependencies, copies app.
- `docker-compose.yml`
  - defines service, ports, env, and mounted data volumes.
- `.env`
  - runtime secrets/config (local only).
- `requirements.txt`
  - pinned package versions.

### Example runtime idea
- Expose app on port `8000`.
- Mount `./data:/app/data` so Chroma persists across restarts.
- Run `scripts/ingest_docs.py` once, then serve API.

### Why Docker helps
- Same environment across your laptop, teammate machine, and server.
- Fewer “works on my machine” issues.
- Easier CI/CD and deployment packaging.

---

## 8) Practical Example Use Case

### Use case: Company Internal Policy Assistant

**Goal:** Employees ask questions about HR, security, leave policy, travel, and onboarding docs.

### Adapted architecture
- Add metadata fields: `department`, `policy_type`, `effective_date`.
- Retriever filter by department when needed.
- Prompt instructs model to cite policy section and effective date.
- Include “escalate to HR” fallback when confidence/context is weak.

---

## 9) Skills You Will Learn

### AI / LLM skills
- Prompt design for grounded QA.
- Embedding strategy and chunking tradeoffs.
- Hallucination reduction through context control.

### Backend / integration skills
- API integration with OpenAI.
- Service-layer architecture with LangChain orchestration.
- Config and dependency management.

### Data pipeline skills
- Document parsing and normalization.
- Metadata modeling and indexing.
- Retrieval testing and quality checks.

### Deployment skills
- Docker image creation and compose orchestration.
- Environment-based configuration.
- Operational scripts for ingest/reindex/smoke tests.

---

## 10) Stretch Improvements (ranked easiest -> advanced)

1. **Metadata filtering** (easy)
2. **Multi-file ingestion pipeline** (easy)
3. **Chat history memory (bounded window)** (easy-medium)
4. **FastAPI backend with `/chat` + `/ingest` endpoints** (medium)
5. **Basic frontend UI (Streamlit/React)** (medium)
6. **Evaluation harness (faithfulness + relevance set)** (medium)
7. **Hybrid retrieval (keyword + vector)** (medium-hard)
8. **Re-ranker layer** (hard)
9. **Cloud deployment (AWS/GCP/Azure)** (hard)
10. **Multi-tenant architecture + auth + access control** (advanced)

---

## Starter Implementation Notes for VS Code

- Create tasks in `.vscode/tasks.json` for:
  - `python scripts/ingest_docs.py`
  - `uvicorn app.main:app --reload --port 8000`
  - `pytest -q`
- Create launch configs in `.vscode/launch.json` for API debugging.
- Keep prompts in files (`prompts/`) so prompt updates don’t require code edits.

---

## Next Action Checklist (Do this first)

1. Create folder skeleton from section 3.
2. Add `.env.example` with required variables.
3. Build `config.py` and `pipeline.py`.
4. Ingest 3–10 real documents.
5. Build retriever + basic `rag_chain.py`.
6. Add simple `/chat` API endpoint.
7. Dockerize and run with `docker compose up`.
8. Record a demo (2–3 mins) for portfolio.

You now have a complete implementation-oriented plan that is beginner-friendly and production-aware.
