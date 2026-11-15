import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base, SessionLocal
from app.models import DocumentMetadata
from app.rag_engine import rag_engine
from app.routes import chat_router, sessions_router, documents_router, bookmarks_router
from app.config import PROJECT_ROOT, BASE_DIR

# Create all database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check if ChromaDB collection is populated or needs seed ingestion
    try:
        count = rag_engine.collection.count()
        print(f"[AI Justice Assistant] ChromaDB active. Existing vector count: {count}")
        if count == 0:
            print("[AI Justice Assistant] Initializing automated vector ingestion from legal_data...")
            result = rag_engine.ingest_all()
            print(f"[AI Justice Assistant] Seed ingestion complete: {result['documents_processed']} docs, {result['total_chunks']} chunks.")
            
            db = SessionLocal()
            try:
                for doc_info in result.get("details", []):
                    new_doc = DocumentMetadata(
                        filename=doc_info["filename"],
                        title=doc_info["title"],
                        file_size_bytes=doc_info["file_size"],
                        chunk_count=doc_info["chunks"]
                    )
                    db.add(new_doc)
                db.commit()
            finally:
                db.close()
    except Exception as e:
        print(f"[AI Justice Assistant] Startup vector check warning: {e}")
    yield
    print("[AI Justice Assistant] Shutting down.")

app = FastAPI(
    title="AI Justice Department Assistant API",
    description="Legal RAG engine for public Indian statutes, acts, regulations, and constitutional provisions.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(documents_router)
app.include_router(bookmarks_router)

@app.get("/api/health")
def health_check():
    vector_count = 0
    try:
        vector_count = rag_engine.collection.count()
    except Exception:
        pass
    return {
        "status": "healthy",
        "service": "AI Justice Department Assistant",
        "jurisdiction": "Republic of India",
        "vector_chunks_indexed": vector_count
    }

# Mount Production Frontend (if built)
candidate_dists = [
    PROJECT_ROOT / "frontend" / "dist",
    BASE_DIR.parent / "frontend" / "dist",
    Path("/app/frontend/dist"),
    Path("./frontend/dist"),
]
for dist_path in candidate_dists:
    if dist_path.exists() and (dist_path / "index.html").exists():
        app.mount("/", StaticFiles(directory=str(dist_path.resolve()), html=True), name="frontend")
        print(f"[AI Justice Assistant] Serving frontend from: {dist_path.resolve()}")
        break

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
