import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Any, Tuple
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import (
    LEGAL_DATA_DIR, 
    CHROMA_PERSIST_DIR, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP, 
    TOP_K_RESULTS
)

COLLECTION_NAME = "indian_legal_statutes"

class LegalRAGEngine:
    def __init__(self):
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        os.makedirs(LEGAL_DATA_DIR, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )

        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"description": "Indian legal statutes, acts, and regulations"}
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", "Section ", "Article ", ". ", " ", ""]
        )

    def extract_document_title(self, filename: str, first_page_text: str) -> str:
        lines = [l.strip() for l in first_page_text.split("\n") if l.strip()]
        for line in lines[:5]:
            upper = line.upper()
            if "THE " in upper or "ACT" in upper or "CONSTITUTION" in upper or "SANHITA" in upper:
                return line
        base = Path(filename).stem.replace("_", " ")
        return base.title()

    def identify_section(self, text: str, fallback_section: str = "General Provision") -> str:
        # Match e.g. "Section 303: Theft", "Article 21: Protection", "Section 20"
        match = re.search(r'\b((?:Section|Article)\s+\d+[A-Za-z]*(?:\s*:\s*[A-Za-z\s,]+)?)', text, re.IGNORECASE)
        if match:
            raw = match.group(1).strip()
            # Clean up trailing words if matched too much
            parts = raw.split("\n")[0]
            return parts[:40].strip()
        return fallback_section

    def ingest_single_file(self, file_path: str) -> Tuple[str, str, int, int]:
        path = Path(file_path)
        filename = path.name
        file_size = os.path.getsize(file_path)
        
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        if total_pages == 0:
            return filename, filename, file_size, 0

        first_page_text = reader.pages[0].extract_text() or ""
        doc_title = self.extract_document_title(filename, first_page_text)

        # Delete existing chunks for this document if re-ingesting
        try:
            self.collection.delete(where={"document_name": filename})
        except Exception:
            pass

        documents_to_add = []
        metadatas_to_add = []
        ids_to_add = []

        last_known_section = "Preliminary Provisions"
        chunk_counter = 0

        for page_idx, page in enumerate(reader.pages):
            page_num = page_idx + 1
            page_text = page.extract_text() or ""
            if not page_text.strip():
                continue

            chunks = self.splitter.split_text(page_text)
            for c_idx, chunk in enumerate(chunks):
                section = self.identify_section(chunk, last_known_section)
                if section != "Preliminary Provisions" and section != "General Provision":
                    last_known_section = section

                # Prepend document and section context so embedding has maximal semantic alignment
                semantic_chunk_text = f"[{doc_title} | {section} | Page {page_num}]\n{chunk}"

                chunk_id = f"{filename}_p{page_num}_c{c_idx}_{chunk_counter}"
                documents_to_add.append(semantic_chunk_text)
                metadatas_to_add.append({
                    "document_name": filename,
                    "title": doc_title,
                    "page": int(page_num),
                    "section": section,
                })
                ids_to_add.append(chunk_id)
                chunk_counter += 1

        if documents_to_add:
            batch_size = 50
            for i in range(0, len(documents_to_add), batch_size):
                end_i = i + batch_size
                self.collection.upsert(
                    documents=documents_to_add[i:end_i],
                    metadatas=metadatas_to_add[i:end_i],
                    ids=ids_to_add[i:end_i]
                )

        return filename, doc_title, file_size, chunk_counter

    def ingest_all(self) -> Dict[str, Any]:
        pdf_pattern = os.path.join(LEGAL_DATA_DIR, "*.pdf")
        pdf_files = glob.glob(pdf_pattern)
        
        results = []
        total_chunks = 0
        for pdf_file in pdf_files:
            fn, title, size, chunks = self.ingest_single_file(pdf_file)
            total_chunks += chunks
            results.append({
                "filename": fn,
                "title": title,
                "file_size": size,
                "chunks": chunks
            })

        return {
            "documents_processed": len(results),
            "total_chunks": total_chunks,
            "details": results
        }

    def retrieve_relevant_chunks(self, query: str, top_k: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
        count = self.collection.count()
        if count == 0:
            return []

        actual_k = min(top_k, count)
        query_results = self.collection.query(
            query_texts=[query],
            n_results=actual_k,
            include=["documents", "metadatas", "distances"]
        )

        citations = []
        if query_results and "documents" in query_results and query_results["documents"]:
            docs = query_results["documents"][0]
            metas = query_results["metadatas"][0]
            dists = query_results["distances"][0] if "distances" in query_results else [0.0] * len(docs)

            for doc_text, meta, dist in zip(docs, metas, dists):
                score = round(max(0.1, 1.0 - (dist / 2.0)), 3)
                
                # Strip semantic header prefix if present for clean display
                cleaned_snippet = doc_text
                if cleaned_snippet.startswith("[") and "]\n" in cleaned_snippet:
                    cleaned_snippet = cleaned_snippet.split("]\n", 1)[1]

                citations.append({
                    "document_name": meta.get("document_name", "Unknown Statute"),
                    "title": meta.get("title", "Legal Document"),
                    "section": meta.get("section", "General Provision"),
                    "page": int(meta.get("page", 1)),
                    "snippet": cleaned_snippet.strip(),
                    "relevance_score": score
                })

        return citations

rag_engine = LegalRAGEngine()
