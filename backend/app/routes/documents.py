import os
import shutil
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import DocumentMetadata
from ..schemas import DocumentItem, IngestResponse
from ..rag_engine import rag_engine
from ..config import LEGAL_DATA_DIR

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.get("", response_model=List[DocumentItem])
def list_documents(db: Session = Depends(get_db)):
    """List all registered legal statute documents."""
    docs = db.query(DocumentMetadata).order_by(DocumentMetadata.title.asc()).all()
    return [
        DocumentItem(
            id=d.id,
            filename=d.filename,
            title=d.title,
            file_size_bytes=d.file_size_bytes,
            chunk_count=d.chunk_count,
            ingested_at=d.ingested_at
        ) for d in docs
    ]

@router.post("/ingest", response_model=IngestResponse)
def trigger_ingestion(db: Session = Depends(get_db)):
    """Trigger ingestion scan over ./legal_data folder."""
    result = rag_engine.ingest_all()
    
    # Sync with DocumentMetadata table
    for doc_info in result.get("details", []):
        existing = db.query(DocumentMetadata).filter(DocumentMetadata.filename == doc_info["filename"]).first()
        if existing:
            existing.title = doc_info["title"]
            existing.file_size_bytes = doc_info["file_size"]
            existing.chunk_count = doc_info["chunks"]
            existing.ingested_at = datetime.utcnow()
        else:
            new_doc = DocumentMetadata(
                filename=doc_info["filename"],
                title=doc_info["title"],
                file_size_bytes=doc_info["file_size"],
                chunk_count=doc_info["chunks"],
                ingested_at=datetime.utcnow()
            )
            db.add(new_doc)
    db.commit()

    return IngestResponse(
        status="success",
        message="Statute ingestion and vectorization completed successfully.",
        documents_processed=result["documents_processed"],
        total_chunks=result["total_chunks"]
    )

@router.post("/upload", response_model=DocumentItem)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a new legal statute PDF and automatically vectorize it."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    os.makedirs(LEGAL_DATA_DIR, exist_ok=True)
    destination_path = os.path.join(LEGAL_DATA_DIR, file.filename)

    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ingest this single uploaded file
    fn, title, size, chunks = rag_engine.ingest_single_file(destination_path)

    existing = db.query(DocumentMetadata).filter(DocumentMetadata.filename == fn).first()
    if existing:
        existing.title = title
        existing.file_size_bytes = size
        existing.chunk_count = chunks
        existing.ingested_at = datetime.utcnow()
        doc_entry = existing
    else:
        doc_entry = DocumentMetadata(
            filename=fn,
            title=title,
            file_size_bytes=size,
            chunk_count=chunks,
            ingested_at=datetime.utcnow()
        )
        db.add(doc_entry)
    db.commit()
    db.refresh(doc_entry)

    return DocumentItem(
        id=doc_entry.id,
        filename=doc_entry.filename,
        title=doc_entry.title,
        file_size_bytes=doc_entry.file_size_bytes,
        chunk_count=doc_entry.chunk_count,
        ingested_at=doc_entry.ingested_at
    )
