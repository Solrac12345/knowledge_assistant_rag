# 📚 Knowledge Assistant RAG

A lightweight, secure Retrieval-Augmented Generation (RAG) API for document question-answering. Built with FastAPI, ChromaDB, and sentence-transformers. Designed for precise semantic retrieval, configurable LLM backends, and production-ready deployment.

## Problem & Solution

**Problem:** Teams store policies, handbooks, and internal docs in long PDFs or text files. Keyword search often misses the right section, and asking a generic LLM risks invented answers that do not match company policy.

**Solution:** This API ingests your documents, splits them into searchable chunks, and answers natural-language questions using only the most relevant retrieved context. You get a small, secure HTTP service—index once, then ask in plain language and receive answers grounded in your own files.

---

## ✨ Features
- 🔍 Semantic vector search with configurable chunking
- 📄 Ingests `.txt`, `.pdf`, and `.docx` documents
- 🔒 Secure by default: API key authentication on all endpoints
- ⚙️ Plug-and-play LLM providers: `dummy` | `ollama` | `openai` | `anthropic`
- 🐳 Fully containerized with Docker Compose
- 📖 Auto-generated OpenAPI docs at `/docs`

## 🛠️ Tech Stack
| Layer | Technology |
|-------|------------|
| Framework | FastAPI + Uvicorn (async) |
| Vector Database | ChromaDB (persistent) |
| Embeddings | `sentence-transformers` |
| Package Manager | `uv` |
| Deployment | Docker Compose |

## 🚀 Quick Start

### Local Development
```bash
git clone <your-repo-url>
cd knowledge_assistant_rag
uv sync --dev
cp .env.example .env   # edit LLM_PROVIDER, API_KEY, etc.
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 🔌 API Usage

All protected endpoints require:

```text
-H "X-API-Key: dev-key-do-not-use-in-production"
```

**Order of operations:** start the server → **index** a document → **ask** questions.

| Step | Endpoint | Terminal output tip |
|------|----------|---------------------|
| Index | `POST /api/v1/rag/index` | Pipe to `python -m json.tool` for formatted JSON |
| Ask | `GET /api/v1/rag/ask?query=...` | Pipe to `python -c "..."` below to print only the answer (plain text, no `\n` escapes) |

**Windows (PowerShell):** use `curl.exe` instead of `curl` (PowerShell aliases `curl` to `Invoke-WebRequest`).

**Questions in the URL:** use `+` for spaces, e.g. `how+many+vacation+days` → `how many vacation days`.

---

### Step 1 — Index a document (run once per file, or to refresh)

Run from the project root in a **second terminal** (keep `uvicorn` running in the first).

Re-uploading the **same filename** replaces its previous chunks in Chroma (no manual cleanup needed).

```bash
curl.exe -s -X POST http://localhost:8000/api/v1/rag/index \
  -H "X-API-Key: dev-key-do-not-use-in-production" \
  -F "file=@employee_handbook_excerpt.txt" | python -m json.tool
```

On Git Bash / Linux / macOS, use `curl` instead of `curl.exe`.

**Expected response:**

```json
{
    "status": "indexed",
    "filename": "employee_handbook_excerpt.txt"
}
```

---

### Step 2 — Ask questions

Use this pattern (replace `YOUR+QUESTION` with a URL-encoded query):

```bash
curl.exe -s "http://localhost:8000/api/v1/rag/ask?query=YOUR+QUESTION" \
  -H "X-API-Key: dev-key-do-not-use-in-production" \
  | python -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

**Full JSON response (optional):** drop the `python -c` pipe and use `| python -m json.tool` instead.

The examples below use `LLM_PROVIDER=dummy` in `.env` and the sample `employee_handbook_excerpt.txt`. With `ollama` / `openai` / `anthropic`, wording may vary but should stay grounded in the handbook.

#### Example 1 — Vacation days

**Question:** `how many vacation days full-time`

```bash
curl.exe -s "http://localhost:8000/api/v1/rag/ask?query=how+many+vacation+days+full-time" \
  -H "X-API-Key: dev-key-do-not-use-in-production" \
  | python -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

**Expected answer:**

```text
All full-time employees are entitled to 15 working days of paid vacation per calendar year.
```

#### Example 2 — Remote work

**Question:** `remote work days per week`

```bash
curl.exe -s "http://localhost:8000/api/v1/rag/ask?query=remote+work+days+per+week" \
  -H "X-API-Key: dev-key-do-not-use-in-production" \
  | python -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

**Expected answer:**

```text
Employees may work remotely up to 3 days per week with manager approval.
```

#### Example 3 — Health insurance (PPO / HMO)

**Question:** `health insurance PPO HMO`

```bash
curl.exe -s "http://localhost:8000/api/v1/rag/ask?query=health+insurance+PPO+HMO" \
  -H "X-API-Key: dev-key-do-not-use-in-production" \
  | python -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

**Expected answer:**

```text
Employees can choose between PPO and HMO plans during open enrollment in November.
```

---

**Troubleshooting**

- **Garbled or wrong answers** — re-run the index command above (same filename), or restart `uvicorn` after code changes, then index again.
- **401 / 403** — check `API_KEY` in `.env` matches the `X-API-Key` header.
- **Empty or generic answers** — confirm the handbook was indexed and `CHROMA_DB_PATH` points to `data/chroma`.

## License

This project is licensed under the [MIT License](LICENSE).

