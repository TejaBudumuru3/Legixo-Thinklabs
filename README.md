# Legixo Thinklabs — Legal Document Q&A API

Legixo Thinklabs is an intelligent legal document research assistant built with **LangGraph**, **Pinecone**, **Google Gemini**, and **Groq (Llama 3.3)**. It provides a RESTful HTTP API for querying legal document corpora with high precision, automatic relevance grading, iterative query rewriting, and grounded citations.

---

##  Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Orchestration** | LangGraph (`StateGraph`) | Agentic graph workflow with conditional looping & retry bounds |
| **Embeddings** | Gemini (`gemini-embedding-001`) | 768-dimensional text embeddings (`RETRIEVAL_DOCUMENT` / `RETRIEVAL_QUERY`) |
| **Vector Database** | Pinecone | Serverless vector index (`legixo-corpus`, cosine similarity) |
| **LLM Inference** | Groq (`llama-3.3-70b-versatile`) | Fast relevance grading (JSON Mode) & grounded answer generation |
| **API Server** | FastAPI & Uvicorn | Async REST API with `POST /ask` endpoint and error handling |
| **Frontend** | Vanilla HTML / CSS / JS | Interactive dark-themed web chat UI |

---

##  Architecture & Pipeline Flow

```
User Query → FastAPI (/ask) → LangGraph Engine:
   │
   ├── 1. retrieval: Embed query via Gemini → Search Pinecone (top_k=5)
   │
   ├── 2. grade: Grade chunk relevance via Groq LLM (JSON Mode)
   │      ├── SUFFICIENT ──→ 3. answer: Synthesize answer & citations → Return
   │      ├── INSUFFICIENT ─→ Rewrite search query (max 3 retries) ──→ Loop to 1
   │      └── NOT_FOUND ────→ Return graceful refusal message → END
```

### Design Decisions

**Why multiple LLM calls?** The requirement for a graph-based workflow with looping/branching inherently requires decoupled steps. The system first grades chunks (1 call) and only synthesizes an answer (1 call) if the grade is sufficient. This separates evaluation from generation, ensuring no hallucinated answers slip through. 

**Isn't this expensive?** The cost is structurally bounded by a strict `MAX_RETRIES = 3` limit. Additionally, the expensive retry loop (generating a rewritten query and re-embedding) only triggers when the initial semantic search fails, meaning easy questions resolve cheaply and hard questions receive proportional effort.

---

##  Quick Start Guide

### Prerequisites
- Python 3.11 or higher
- Pinecone API Key
- Google Gemini API Key
- Groq API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TejaBudumuru3/Legixo-Thinklabs.git
   cd Legixo-Thinklabs
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   GEMINI_API=your_gemini_api_key
   PINECONE_API=your_pinecone_api_key
   GROQ_API=your_groq_api_key
   ```

5. **Ingest the corpus into Pinecone:**
   ```bash
   python ingest.py
   ```
   *This reads all markdown files from `corpus/`, splits them into 250-character chunks, generates embeddings using Gemini, and uploads them to Pinecone.*

6. **Start the API server:**
   ```bash
   uvicorn app.api.app:app --reload
   ```
   - Web Chat Interface: `http://localhost:8000/`
   - API Endpoint: `http://localhost:8000/ask`
   - Interactive API Docs: `http://localhost:8000/docs`

---

##  API Usage

### `POST /ask`

**Request Header:** `Content-Type: application/json`

**Request Body:**
```json
{
  "question": "What notice period applies when Bluecrest or Priya Nambiar ends the employment agreement?"
}
```

**Response Body (`200 OK`):**
```json
{
  "answer": "The notice period that applies when Bluecrest or Priya Nambiar ends the employment agreement is \"60 days\" as stated in the \"Notice period\" section...",
  "citations": [
    "02_employment_agreement_excerpt.md"
  ],
  "trace": {
    "final_grade": "SUFFICIENT",
    "retries": 0
  }
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How long is the non-compete after leaving Bluecrest?"}'
```

---

##  Evaluation & Self-Testing

Run the comprehensive 23-test evaluation suite:
```bash
python eval/run_test.py
```
Results will be saved to `eval/test_results.json`.

---

## 📁 Project Structure

```
Legixo-Thinklabs/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py              # FastAPI application & routes
│   ├── __init__.py
│   ├── graph.py                # LangGraph StateGraph & conditional routing
│   ├── nodes.py                # Graph nodes (retrieval, grade, answer)
│   ├── pinecone_client.py      # Pinecone query & upsert client
│   ├── prompts.py              # Prompt templates for LLM
│   └── state.py                # GraphState TypedDict & Pydantic models
├── corpus/                     # 6 legal markdown documents
├── docs/
│   └── langgraph.md            # Detailed pipeline documentation & Mermaid diagram
├── eval/
│   ├── run_test.py             # Automated test execution script
│   ├── test_cases.json         # 23 evaluation test cases
│   └── test_results.json       # Generated test execution results
├── static/
│   └── index.html              # Web Chat UI
├── config.py                   # API key loader & client initialization
├── ingest.py                   # Corpus chunking, embedding & Pinecone ingestion
├── requirements.txt            # Dependencies
├── .env.example                # Environment variables template
└── README.md                   # Project documentation
```

---

##  License

MIT License. Built as an Agentic RAG technical assessment.
