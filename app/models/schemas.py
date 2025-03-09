from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

# ========== Request Models ==========

class ChatMessage(BaseModel):
    """Model for chat messages"""
    role: str
    content: str


class CreateSessionRequest(BaseModel):
    """Model for creating a new session"""
    user_id: Optional[str] = None


class UpdateSessionTitleRequest(BaseModel):
    """Model for updating session title"""
    title: str


# ========== Response Models ==========

class CreateSessionResponse(BaseModel):
    """Response model for session creation"""
    session_id: str


class SessionResponse(BaseModel):
    """Response model for session information"""
    session_id: str
    user_id: Optional[str]
    title: str
    created_at: str
    updated_at: str
    message_count: int
    is_active: bool


class StatusResponse(BaseModel):
    """Response model for status information"""
    status: str
    version: str
    sessions: int
    connections: int
    model: str


class MessageResponse(BaseModel):
    """Response model for a message"""
    id: str
    role: str
    content: str
    timestamp: str 