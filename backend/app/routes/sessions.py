import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import ChatSession, ChatMessage
from ..schemas import (
    SessionResponse, 
    SessionDetailResponse, 
    SessionCreate, 
    MessageResponse, 
    CitationItem
)

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])

@router.get("", response_model=List[SessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    """List all chat sessions ordered by latest updated."""
    sessions = db.query(ChatSession).order_by(ChatSession.updated_at.desc()).all()
    
    results = []
    for s in sessions:
        msg_count = db.query(func.count(ChatMessage.id)).filter(ChatMessage.session_id == s.id).scalar() or 0
        results.append(SessionResponse(
            id=s.id,
            title=s.title,
            created_at=s.created_at,
            updated_at=s.updated_at,
            message_count=msg_count
        ))
    return results

@router.post("", response_model=SessionResponse)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    """Create a new chat session."""
    session = ChatSession(title=payload.title or "New Legal Inquiry")
    db.add(session)
    db.commit()
    db.refresh(session)
    return SessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        message_count=0
    )

@router.get("/{session_id}", response_model=SessionDetailResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    """Get a single session and its full message history."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()

    formatted_messages = []
    for m in messages:
        cits = None
        if m.citations_json:
            try:
                raw_cits = json.loads(m.citations_json)
                cits = [CitationItem(**c) for c in raw_cits]
            except Exception:
                cits = []
        formatted_messages.append(MessageResponse(
            id=m.id,
            session_id=m.session_id,
            role=m.role,
            content=m.content,
            citations=cits,
            created_at=m.created_at
        ))

    return SessionDetailResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        message_count=len(formatted_messages),
        messages=formatted_messages
    )

@router.delete("/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a chat session and all messages."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"status": "success", "message": f"Session {session_id} deleted."}
