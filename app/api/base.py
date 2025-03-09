from fastapi import APIRouter

from app.models.schemas import StatusResponse
from app.services.session_manager import session_manager
from app.config import APP_VERSION, LLM_MODEL_NAME

# Create router
router = APIRouter()

@router.get("/", response_model=StatusResponse)
async def root():
    """Root endpoint that returns status information"""
    return {
        "status": "online",
        "version": APP_VERSION,
        "sessions": session_manager.get_session_count(),
        "connections": session_manager.get_connection_count(),
        "model": LLM_MODEL_NAME
    } 