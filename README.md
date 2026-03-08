# 📋 Company Policy Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that lets employees query company policy documents using natural language — filtered by department, region, policy type, and year.

Built with **LangChain · ChromaDB · Gemini · Streamlit · BAAI/bge-small-en-v1.5**

---

## 🗂️ Project Structure

```
rag-policy-chatbot/
├── data/
│   ├── india_leave_policy_2024.pdf
│   ├── us_expense_policy_2024.pdf
│   └── metadata_manifest.json      # Maps filenames → metadata
├── chroma_db/                       # Auto-generated vector store (gitignored)
├── src/
│   ├── __init__.py
│   ├── config.py                    # All constants and env vars
│   ├── embeddings.py                # Embedding model setup
│   ├── ingest.py                    # Indexing pipeline
│   ├── retriever.py                 # Filtered retrieval logic
│   └── chain.py                     # LangChain QA chain
├── tests/
│   ├── test_embedding.py
│   ├── test_retriever.py
│   └── test_end_to_end.py
├── app.py                           # Streamlit frontend
├── check.py                         # Quick ChromaDB health check
├── pytest.ini
├── requirement.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

| Component | Tool |
|---|---|
| Orchestration | LangChain |
| Vector Database | ChromaDB |
| LLM | Gemini 2.5 Flash (Google) |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Frontend | Streamlit |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/rag-policy-chatbot.git
cd rag-policy-chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

### 4. Set up your environment variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

> Get your free Gemini API key at [aistudio.google.com](https://aistudio.google.com)

### 5. Build the vector index

This reads the PDFs, chunks them, embeds them, and stores everything in ChromaDB. Run this once before starting the app (and again whenever you add new documents).

```bash
python -m src.ingest
```

Expected output:
```
Loading: data/india_leave_policy_2024.pdf
Loading: data/us_expense_policy_2024.pdf
Total chunks created: 87
Index built! 87 vectors stored.
```

### 6. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💬 Example Usage

**Question:** `What is the leave policy for employees in India?`

**Filters selected:**
- Department: `HR`
- Region: `India`
- Policy Type: `Leave`
- Year: `2024`

**Answer:** The chatbot retrieves only India HR Leave policy chunks and generates a grounded answer with source citations.

---

## 📁 Adding New Policy Documents

1. Place the PDF or DOCX file in the `data/` folder.

2. Add an entry to `data/metadata_manifest.json`:

```json
{
  "filename": "uk_data_privacy_2024.pdf",
  "department": "Legal",
  "region": "UK",
  "policy_type": "Data Privacy",
  "effective_year": 2024
}
```

3. Re-run the ingestion pipeline:

```bash
python -m src.ingest
```

Supported file formats: `.pdf`, `.txt`, `.md`, `.docx`

---

## 🔍 Verify the Index

If you want to quickly check that ChromaDB was populated correctly:

```bash
python check.py
```

This prints the total number of stored chunks and a sample document with its metadata.

---

## 🧪 Running Tests

```bash
pytest tests/
```

| Test File | What it Tests |
|---|---|
| `test_embedding.py` | Embedding shape (384-dim) and semantic similarity |
| `test_retriever.py` | Filter construction logic (single, multiple, none) |
| `test_end_to_end.py` | Full pipeline: retrieval + LLM + source metadata validation |

> **Note:** `test_end_to_end.py` requires the ChromaDB index to be built (`python -m src.ingest`) and a valid `GOOGLE_API_KEY` in `.env` before running.

---

## 🏗️ How It Works

### Indexing Pipeline (run once)

```
PDF / DOCX files
      ↓
Load with LangChain DocumentLoaders
      ↓
Split into chunks (500 tokens, 50 overlap)
      ↓
Attach metadata (department, region, policy_type, year)
      ↓
Embed with BAAI/bge-small-en-v1.5
      ↓
Store in ChromaDB (persisted to disk)
```

### Query Pipeline (every user question)

```
User question + sidebar filters
      ↓
Build ChromaDB where-clause filter
      ↓
Semantic search (MMR) on filtered chunks
      ↓
Top-5 chunks passed as context to Gemini
      ↓
Grounded answer + source citations → Streamlit UI
```

---

## 🔧 Configuration

All settings are in `src/config.py`:

| Variable | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | `500` | Tokens per document chunk |
| `OVERLAP_SIZE` | `50` | Overlap between consecutive chunks |
| `TOP_K` | `5` | Number of chunks retrieved per query |
| `EMBED_MODEL` | `BAAI/bge-small-en-v1.5` | HuggingFace embedding model |
| `LLM_MODEL` | `gemini-2.5-flash` | Gemini model name |
| `LLM_TEMPERATURE` | `0.1` | Lower = more factual responses |
| `COLLECTION_NAME` | `policy_documents` | ChromaDB collection name |

---

## 🚢 Deployment (Streamlit Community Cloud)

1. Push your project to a **public GitHub repository** (ChromaDB index included, or add an init step).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select your repo → set main file to `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```
   GOOGLE_API_KEY = "your_key_here"
   ```
5. Click **Deploy**.

---

## 🛠️ Troubleshooting

**`404 NOT_FOUND` error from Gemini**
→ The model name is wrong. Check `LLM_MODEL` in `config.py`. Valid values: `gemini-2.5-flash`, `gemini-2.5-pro`. Run `python -c "import google.generativeai as g; g.configure(api_key='YOUR_KEY'); [print(m.name) for m in g.list_models()]"` to list all available models for your key.

**`AssertionError: Should return source documents`**
→ The ChromaDB index is empty or not built yet. Run `python -m src.ingest` first, then re-run tests.

**Metadata filter returns no results**
→ Metadata keys must match exactly (case-sensitive). Run `python check.py` and inspect the printed metadata to confirm the exact key names stored in ChromaDB.

**HuggingFace model download is slow**
→ The embedding model (~130MB) downloads once on first run and is cached in `~/.cache/huggingface/`. Subsequent runs are instant.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.