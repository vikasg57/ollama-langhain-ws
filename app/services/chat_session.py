from typing import Dict, List, Optional
from datetime import datetime
import uuid
from fastapi import WebSocket

from app.logging_config import logger

class ChatSession:
    """Chat session manager for a single chat"""

    def __init__(self, session_id: str, user_id: Optional[str] = None):
        """Initialize a new chat session"""
        self.session_id = session_id
        self.user_id = user_id
        self.messages: List[Dict] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = "New Chat"  # Default title
        self.active_connection = None

    def add_message(self, role: str, content: str) -> Dict:
        """Add a message to the session"""
        message = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message

    def get_history_text(self, limit: int = 10) -> str:
        """Get formatted conversation history for prompt context"""
        recent_messages = self.messages[-limit * 2:] if self.messages else []
        formatted_history = []

        for msg in recent_messages:
            role = "Kid" if msg["role"] == "user" else "Tutor"
            formatted_history.append(f"{role}: {msg['content']}")

        return "\n".join(formatted_history)

    def set_connection(self, websocket: WebSocket):
        """Set the active WebSocket connection"""
        self.active_connection = websocket

    def clear_connection(self):
        """Clear the active WebSocket connection"""
        self.active_connection = None

    def is_connected(self) -> bool:
        """Check if session has an active connection"""
        return self.active_connection is not None

    def update_title(self, title: str):
        """Update session title"""
        self.title = title
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convert session to dictionary"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_count": len(self.messages),
            "is_active": self.is_connected()
        } 