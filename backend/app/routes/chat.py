import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ChatSession, ChatMessage
from ..schemas import ChatRequest, ChatResponse, CitationItem
from ..rag_engine import rag_engine
from ..llm_service import generate_legal_answer

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
async def handle_legal_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    session_id = payload.session_id
    session = None

    if session_id:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()

    # Create new session if none provided or not found
    if not session:
        session_title = query[:48] + "..." if len(query) > 48 else query
        session = ChatSession(title=session_title)
        db.add(session)
        db.commit()
        db.refresh(session)
        session_id = session.id

    # 1. Save user message to database
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        content=query,
        created_at=datetime.utcnow()
    )
    db.add(user_msg)

    # 2. Retrieve top-4 relevant legal chunks from ChromaDB
    citations_data = rag_engine.retrieve_relevant_chunks(query, top_k=4)

    # 3. Generate answer using Gemini / Fallback with strict anti-hallucination prompt
    answer = generate_legal_answer(query, citations_data)

    # 4. Save assistant response with citations to database
    assistant_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=answer,
        citations_json=json.dumps(citations_data),
        created_at=datetime.utcnow()
    )
    db.add(assistant_msg)

    # Update session timestamp
    session.updated_at = datetime.utcnow()
    db.commit()

    # Format response
    citation_items = [CitationItem(**c) for c in citations_data]

    return ChatResponse(
        session_id=session_id,
        query=query,
        answer=answer,
        citations=citation_items,
        created_at=assistant_msg.created_at
    )
