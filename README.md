# AI Justice Department Assistant (Nyaya Assistant)

An authoritative, government-grade **Legal Retrieval-Augmented Generation (RAG) Web Application** designed specifically for public Indian statutes, Parliamentary Acts, regulations, and constitutional provisions.

Built with a modern **React.js + Tailwind CSS** frontend, a high-performance **Python FastAPI** backend, a locally persisted **ChromaDB** vector database powered by `sentence-transformers/all-MiniLM-L6-v2`, and a relational **SQLite (SQLAlchemy)** store for sessions, chat transcripts, and bookmarked legal answers.

---

## 🏛️ System Architecture

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │                  React.js Frontend (Vite)              │
                                  │  - ChatGPT-style Interface with Dark/Light Mode        │
                                  │  - Expandable Source Citation Drawers                  │
                                  │  - Legal Document Vault (Upload & Ingest)              │
                                  │  - Session History & Legal Bookmarks Drawer            │
                                  │  - Markdown & PDF / Print Exporters                    │
                                  └──────────────────────────┬─────────────────────────────┘
                                                             │ Axios (REST API / Proxy)
                                                             ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │               FastAPI Asynchronous Backend             │
                                  │  - POST /api/chat           - GET/POST /api/documents  │
                                  │  - GET/POST /api/sessions   - GET/POST /api/bookmarks  │
                                  └───────────────┬──────────────────────────┬─────────────┘
                                                  │                          │
                 ┌────────────────────────────────┴────────┐                 │
                 ▼                                         ▼                 ▼
   ┌───────────────────────────┐             ┌───────────────────────────┐  ┌─────────────────────────┐
   │ ChromaDB Vector Storage   │             │   SQLAlchemy Database     │  │ LLM Generation Engine   │
   │ - Collection:             │             │   (SQLite: app_data.db)   │  │ - Google Gemini 1.5     │
   │   indian_legal_statutes   │             │ - ChatSession             │  │   Flash via API Key     │
   │ - Embeddings:             │             │ - ChatMessage (Citations) │  │ - Strict Anti-          │
   │   all-MiniLM-L6-v2 (ONNX) │             │ - Bookmark (Annotations)  │  │   Hallucination System  │
   │ - Recursive Chunking      │             │ - DocumentMetadata        │  │   Prompt                │
   │   (size: 1000, ovlp: 200) │             └───────────────────────────┘  │ - Deterministic Legal   │
   └─────────────▲─────────────┘                                            │   Synthesis Fallback    │
                 │                                                          └─────────────────────────┘
   ┌─────────────┴─────────────┐
   │    ./legal_data Folder    │
   │ - BNS 2023 (Penal Code)   │
   │ - IT Act 2000 (Cyber Law) │
   │ - RTI Act 2005            │
   │ - Constitution Part III   │
   │ - DPDP Act 2023 (Privacy) │
   └───────────────────────────┘
```

---

## 📁 Repository Structure

```
ai-justice-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py              # Environment configuration & paths
│   │   ├── database.py            # SQLite engine, sessionmaker & Base
│   │   ├── models.py              # ChatSession, ChatMessage, Bookmark, DocumentMetadata
│   │   ├── schemas.py             # Pydantic v2 schemas for requests & responses
│   │   ├── rag_engine.py          # PDF parser, RecursiveCharacterTextSplitter, ChromaDB
│   │   ├── llm_service.py         # Gemini 1.5 Flash client & strict anti-hallucination engine
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── chat.py            # POST /api/chat (Retrieval + Generation + Citations)
│   │       ├── sessions.py        # GET, POST, DELETE /api/sessions
│   │       ├── documents.py       # GET, POST /api/documents (List, Ingest, Upload PDF)
│   │       └── bookmarks.py       # GET, POST, DELETE /api/bookmarks
│   ├── scripts/
│   │   └── generate_legal_data.py # PDF generator for Indian statutory acts
│   ├── main.py                    # FastAPI server entry point with startup auto-ingestion
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Template environment configuration
│   └── app_data.db                # SQLite relational database
├── frontend/
│   ├── index.html                 # Government-grade title & font styling
│   ├── package.json               # React, Tailwind, Lucide React, Axios
│   ├── vite.config.js             # Vite build configuration with /api backend proxy
│   ├── tailwind.config.js         # Custom justice & gold color palette
│   ├── postcss.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx                # Application state, layout, session management
│       ├── index.css              # Tailwind base, dark mode, custom scrollbars
│       ├── api.js                 # Axios API service client
│       └── components/
│           ├── Navbar.jsx         # Tri-color emblem banner, theme toggle, vector badge
│           ├── Sidebar.jsx        # ChatGPT-style inquiry history & utility navigation
│           ├── ChatWindow.jsx     # Chat stream, suggestions, input bar & disclaimer
│           ├── MessageItem.jsx    # Markdown renderer, copy, bookmark trigger
│           ├── SourceCard.jsx     # Expandable legal citation drawer with match %
│           ├── DocumentModal.jsx  # Legal Document Vault (admin/user statute manager)
│           ├── BookmarksModal.jsx # Saved legal provisions & annotated research
│           └── ExportModal.jsx    # Markdown (.md) and Print-to-PDF exporters
├── legal_data/                    # Authentic PDF Statutes repository
│   ├── Bharatiya_Nyaya_Sanhita_2023.pdf
│   ├── Information_Technology_Act_2000.pdf
│   ├── Right_to_Information_Act_2005.pdf
│   ├── Constitution_of_India_Fundamental_Rights.pdf
│   └── Digital_Personal_Data_Protection_Act_2023.pdf
├── chroma_db/                     # Persistent ChromaDB vector index
└── README.md                      # Documentation
```

---

## ⚡ Key Features

### 1. Document Ingestion & Vectorization Module
* **Automated Directory Scanner:** Scans `./legal_data` for all PDF statutes, Acts of Parliament, and government legal gazettes.
* **Legal Text Chunking:** Employs LangChain's `RecursiveCharacterTextSplitter` with `chunk_size=1000` and `chunk_overlap=200`, with separators that prioritize section boundaries (`Section `, `Article `).
* **Local Embeddings (ChromaDB + ONNX):** Embeds all document chunks using `sentence-transformers/all-MiniLM-L6-v2` via high-speed ONNX runtime (384 dimensions, zero heavy CUDA initialization lag).
* **Metadata Attribution:** Every chunk stores `document_name`, `title`, `section` (e.g., *Section 303: Theft*, *Article 21*), and `page` number.

### 2. RAG Legal Query Engine (`POST /api/chat`)
1. **Semantic Search:** Retrieves the top 4 most relevant legal chunks from ChromaDB based on cosine similarity.
2. **Relevance Scoring:** Computes transparent match scores (e.g., `85% Match`) for each source chunk.
3. **Strict Anti-Hallucination Directives:**
   * Answers are strictly restricted to the verified context retrieved from ChromaDB.
   * If the context lacks information, the engine explicitly outputs: *"The provided legal statutes do not contain sufficient information to answer this question accurately."*
   * Fabricated sections, non-existent article numbers, or invented penalties are completely prohibited.
4. **Exact Source Citations:** Every response returns an array of structured citations including Act Title, Section, Page number, and snippet.

### 3. Full-Stack User Interface
* **ChatGPT-Style Layout:** Collapsible sidebar for previous chat sessions, new inquiry creation, and instant session switching.
* **Expandable Source Cards:** Expandable drawer cards beneath each AI response displaying Act title, section badge, page badge, relevance match %, and the full statutory text snippet.
* **Document Vault Modal:** Admin/user view to inspect all loaded statutes, file sizes, chunk counts, and upload new PDF acts dynamically with immediate vectorization.
* **Saved Legal Provisions (Bookmarks):** Save any response or statute clause with personalized annotations.
* **Export Utilities:** Instant one-click copy, download inquiry transcript as Markdown (`.md`), or format for printing to official PDF.
* **Indian Government Aesthetic:** Ashoka blue palette (`#0f2062`), gold highlights, subtle tri-color header accent, and dark/light mode toggle.

---

## 🚀 Quick Start Guide

### Prerequisites
* **Python 3.10+** (tested on Python 3.13)
* **Node.js 18+** & **npm**

---

### Step 1: Backend Setup

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Configure Google Gemini API Key in `.env`:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   ```ini
   GOOGLE_API_KEY=your_gemini_api_key_here
   LLM_MODEL=gemini-1.5-flash
   ```
   > **Note:** If `GOOGLE_API_KEY` is not provided, the application runs using its built-in **Deterministic Legal Synthesis Engine**, which processes the retrieved vector chunks accurately with exact sections, definitions, and citations.

4. Start the FastAPI backend server:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
   * The server runs at `http://127.0.0.1:8000`.
   * Interactive Swagger API docs are available at `http://127.0.0.1:8000/docs`.
   * On startup, the server automatically vectorizes any PDF acts located in `./legal_data`.

---

### Step 2: Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   * Open `http://localhost:5173` in your browser.
   * Vite proxies all `/api` requests to `http://127.0.0.1:8000`.

---

## 🧪 Sample Inquiries to Try

* **Bharatiya Nyaya Sanhita (BNS 2023):**
  > *"What are the punishments for theft and murder under Bharatiya Nyaya Sanhita?"*
* **Information Technology Act 2000:**
  > *"What are the penalties for identity theft and hacking under Sections 43 and 66C of the IT Act?"*
* **Right to Information Act 2005:**
  > *"What is the statutory timeline for disposing of an RTI application, and what penalty applies under Section 20?"*
* **Constitution of India (Fundamental Rights):**
  > *"Explain the scope of Right to Life and Personal Liberty under Article 21 and the right against self-incrimination under Article 20."*
* **Digital Personal Data Protection Act 2023:**
  > *"What are the conditions for valid consent and the penalties for personal data breach under the DPDP Act?"*

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health status and number of indexed vector chunks |
| `POST` | `/api/chat` | Send a legal query; returns AI answer and top 4 citations |
| `GET` | `/api/sessions` | List all previous chat sessions |
| `POST` | `/api/sessions` | Create a new chat session |
| `GET` | `/api/sessions/{id}` | Retrieve session history with all citations |
| `DELETE` | `/api/sessions/{id}` | Delete a session and its message history |
| `GET` | `/api/documents` | List all ingested legal acts and chunk counts |
| `POST` | `/api/documents/ingest` | Trigger full re-ingestion of `./legal_data` |
| `POST` | `/api/documents/upload` | Upload a new `.pdf` statute and vectorize immediately |
| `GET` | `/api/bookmarks` | List all bookmarked legal answers |
| `POST` | `/api/bookmarks` | Save an answer as a bookmark with optional note |
| `DELETE` | `/api/bookmarks/{id}` | Remove a bookmark |

---

## ⚖️ Legal Disclaimer

This assistant is an automated computational retrieval and analysis tool developed for public informational and reference purposes only. It does not constitute formal legal representation, statutory certification, or a binding judicial interpretation. For judicial submissions and formal advisory work, always verify citations against the official Gazette of India and authoritative publications of the Ministry of Law and Justice, Government of India.
