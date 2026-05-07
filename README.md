# 📚 Knowledge Assistant RAG

A lightweight, secure Retrieval-Augmented Generation (RAG) API for document question-answering. Built with FastAPI, ChromaDB, and sentence-transformers. Designed for precise semantic retrieval, configurable LLM backends, and production-ready deployment.

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

### 🔌 API Usage
All protected endpoints require: -H "X-API-Key: dev-key-do-not-use-in-production"

### Index a Document in other terminal
curl -X POST http://localhost:8000/api/v1/rag/index \
  -H "X-API-Key: dev-key-do-not-use-in-production" \
  -F "file=@employee_handbook_excerpt.txt"

✅ Response: {"status":"indexed","filename":"employee_handbook_excerpt.txt"}

### Ask a Question
1. curl "http://localhost:8000/api/v1/rag/ask?query=how+many+vacation+days+full-time" \
  -H "X-API-Key: dev-key-do-not-use-in-production"

✅ Expected context: "All full-time employees are entitled to 15 working days of paid vacation per calendar year."

2. curl -s "http://localhost:8000/api/v1/rag/ask?query=remote+work+days+per+week" \
  -H "X-API-Key: dev-key-do-not-use-in-production" | python -m json.tool

 ✅ Expected context: "Employees may work remotely up to 3 days per week with manager approval."

3. curl -s "http://localhost:8000/api/v1/rag/ask?query=health+insurance+PPO+HMO" \
  -H "X-API-Key: dev-key-do-not-use-in-production" | python -m json.tool

 ✅ Expected context: "Employees can choose between PPO and HMO plans during open enrollment in November."  



