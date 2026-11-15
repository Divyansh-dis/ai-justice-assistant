from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Bookmark
from ..schemas import BookmarkCreate, BookmarkResponse

router = APIRouter(prefix="/api/bookmarks", tags=["Bookmarks"])

@router.get("", response_model=List[BookmarkResponse])
def get_bookmarks(db: Session = Depends(get_db)):
    """Retrieve all bookmarked legal answers."""
    bookmarks = db.query(Bookmark).order_by(Bookmark.created_at.desc()).all()
    return [
        BookmarkResponse(
            id=b.id,
            session_id=b.session_id,
            message_id=b.message_id,
            query=b.query,
            answer=b.answer,
            statute_title=b.statute_title,
            section_ref=b.section_ref,
            note=b.note,
            created_at=b.created_at
        ) for b in bookmarks
    ]

@router.post("", response_model=BookmarkResponse)
def add_bookmark(payload: BookmarkCreate, db: Session = Depends(get_db)):
    """Bookmark a legal answer for quick future reference."""
    bookmark = Bookmark(
        session_id=payload.session_id,
        message_id=payload.message_id,
        query=payload.query,
        answer=payload.answer,
        statute_title=payload.statute_title,
        section_ref=payload.section_ref,
        note=payload.note
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return BookmarkResponse(
        id=bookmark.id,
        session_id=bookmark.session_id,
        message_id=bookmark.message_id,
        query=bookmark.query,
        answer=bookmark.answer,
        statute_title=bookmark.statute_title,
        section_ref=bookmark.section_ref,
        note=bookmark.note,
        created_at=bookmark.created_at
    )

@router.delete("/{bookmark_id}")
def delete_bookmark(bookmark_id: str, db: Session = Depends(get_db)):
    """Remove a bookmark by ID."""
    b = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(b)
    db.commit()
    return {"status": "success", "message": f"Bookmark {bookmark_id} deleted."}
