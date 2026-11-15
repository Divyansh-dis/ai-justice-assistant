from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Citation Schema
class CitationItem(BaseModel):
    document_name: str
    title: str
    section: str
    page: int
    snippet: str
    relevance_score: float

# Chat Schemas
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The legal query or question")
    session_id: Optional[str] = Field(None, description="Chat session ID. If omitted, a new session is created.")

class ChatResponse(BaseModel):
    session_id: str
    query: str
    answer: str
    citations: List[CitationItem]
    created_at: datetime

# Message Schema
class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    citations: Optional[List[CitationItem]] = None
    created_at: datetime

# Session Schemas
class SessionCreate(BaseModel):
    title: Optional[str] = "New Legal Inquiry"

class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0

class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse]

# Bookmark Schemas
class BookmarkCreate(BaseModel):
    session_id: Optional[str] = None
    message_id: Optional[str] = None
    query: str
    answer: str
    statute_title: Optional[str] = None
    section_ref: Optional[str] = None
    note: Optional[str] = None

class BookmarkResponse(BaseModel):
    id: str
    session_id: Optional[str]
    message_id: Optional[str]
    query: str
    answer: str
    statute_title: Optional[str]
    section_ref: Optional[str]
    note: Optional[str]
    created_at: datetime

# Document Schemas
class DocumentItem(BaseModel):
    id: str
    filename: str
    title: str
    file_size_bytes: int
    chunk_count: int
    ingested_at: datetime

class IngestResponse(BaseModel):
    status: str
    message: str
    documents_processed: int
    total_chunks: int
