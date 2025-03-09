from typing import Dict, List, Optional
import uuid
import asyncio
from fastapi import WebSocket

from app.services.chat_session import ChatSession
from app.logging_config import logger

class SessionManager:
    """Manager for all chat sessions"""

    def __init__(self):
        """Initialize the session manager"""
        self.sessions: Dict[str, ChatSession] = {}
        self.user_sessions: Dict[str, List[str]] = {}  # user_id -> [session_ids]
        self.connections: Dict[WebSocket, str] = {}  # websocket -> session_id

    def create_session(self, user_id: Optional[str] = None) -> ChatSession:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id, user_id)
        self.sessions[session_id] = session

        if user_id:
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = []
            self.user_sessions[user_id].append(session_id)

        logger.info(f"Created new session {session_id} for user {user_id}")
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a session by ID"""
        return self.sessions.get(session_id)

    def get_user_sessions(self, user_id: str) -> List[ChatSession]:
        """Get all sessions for a user"""
        session_ids = self.user_sessions.get(user_id, [])
        return [self.sessions[sid] for sid in session_ids if sid in self.sessions]

    async def connect(self, websocket: WebSocket, session_id: str) -> ChatSession:
        """Connect a WebSocket to a session"""
        await websocket.accept()

        # Create new session if needed
        if session_id not in self.sessions:
            session = self.create_session()
            session_id = session.session_id
        else:
            session = self.sessions[session_id]

        # Handle existing connection for this session
        if session.is_connected():
            try:
                # Inform the old connection it's being replaced
                await session.active_connection.send_text(
                    "This session has been opened in another window. Disconnecting this instance."
                )
                await session.active_connection.close()
            except Exception:
                # Old connection might already be closed
                pass

        # Set new connection
        session.set_connection(websocket)
        self.connections[websocket] = session_id

        logger.info(f"Connected to session {session_id}")
        return session

    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket"""
        if websocket in self.connections:
            session_id = self.connections[websocket]
            if session_id in self.sessions:
                self.sessions[session_id].clear_connection()
            del self.connections[websocket]
            logger.info(f"Disconnected from session {session_id}")

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]

            # Remove from user_sessions
            if session.user_id and session.user_id in self.user_sessions:
                if session_id in self.user_sessions[session.user_id]:
                    self.user_sessions[session.user_id].remove(session_id)

            # Close connection if active
            if session.is_connected():
                # Don't wait for this to complete
                asyncio.create_task(session.active_connection.close())

            # Remove from connections
            for ws, sid in list(self.connections.items()):
                if sid == session_id:
                    del self.connections[ws]

            # Delete session
            del self.sessions[session_id]
            logger.info(f"Deleted session {session_id}")
            return True
        return False

    def get_connection_count(self) -> int:
        """Get count of active connections"""
        return len(self.connections)

    def get_session_count(self) -> int:
        """Get count of sessions"""
        return len(self.sessions)

# Initialize session manager
session_manager = SessionManager() 