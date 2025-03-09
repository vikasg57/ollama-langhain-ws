from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import List

from app.models.schemas import (
    CreateSessionRequest, 
    CreateSessionResponse, 
    UpdateSessionTitleRequest,
    SessionResponse
)
from app.services.session_manager import session_manager
from app.logging_config import logger

# Create router
router = APIRouter()

@router.post("/sessions", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    """Create a new chat session"""
    session = session_manager.create_session(request.user_id)
    return {"session_id": session.session_id}


@router.get("/sessions/{user_id}", response_model=List[SessionResponse])
async def get_user_sessions(user_id: str):
    """Get all sessions for a user"""
    sessions = session_manager.get_user_sessions(user_id)
    return [session.to_dict() for session in sessions]


@router.put("/sessions/{session_id}/title")
async def update_session_title(session_id: str, request: UpdateSessionTitleRequest):
    """Update a session title"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.update_title(request.title)
    return {"status": "success"}


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_manager.delete_session(session_id):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Session not found")


@router.get("/chat/{session_id}", response_class=HTMLResponse)
async def get_chat_page(session_id: str, request: Request):
    """Get chat page HTML"""
    with open("templates/chat.html", "r") as file:
        return HTMLResponse(content=file.read())


@router.get("/chat", response_class=HTMLResponse)
async def get_new_chat_page():
    """Create a new session and redirect to chat page"""
    session = session_manager.create_session()
    return await get_chat_page(session.session_id, None) 