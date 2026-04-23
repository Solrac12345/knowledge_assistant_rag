# RAG Knowledge Assistant (Python 3.11+, FastAPI, ChromaDB)

A Mid-Pro level Retrieval-Augmented Generation (RAG) system built with modern Python standards, clean architecture, and production-oriented engineering practices.


## 🚀 Project Overview

**EN:**  
This project implements a modular, scalable RAG pipeline using FastAPI, ChromaDB, and modern embedding models.  
It is designed following professional engineering standards: testing, CI/CD, security, and clean architecture.

**FR:**  
Ce projet implémente un pipeline RAG modulaire et scalable utilisant FastAPI, ChromaDB et des modèles d'embedding modernes.  
Il est conçu selon des standards d’ingénierie professionnels : tests, CI/CD, sécurité et architecture propre.

## 🧱 Tech Stack

- Python 3.11+
- FastAPI
- ChromaDB
- Sentence-Transformers
- Pydantic v2
- Pytest
- Ruff + Mypy
- GitHub Actions (CI/CD)


---

## ⚙️ Setup (Bash)

```bash
uv venv
source .venv/bin/activate
uv sync
uvicorn app.main:app --reload

Running Tests
- pytest

Environment Variables
- .env.example.