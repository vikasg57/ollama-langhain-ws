from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import (
    CORS_ORIGINS, 
    CORS_ALLOW_CREDENTIALS, 
    CORS_ALLOW_METHODS, 
    CORS_ALLOW_HEADERS,
    HOST,
    PORT,
    RELOAD
)
from app.api.base import router as base_router
from app.api.sessions import router as sessions_router
from app.api.websocket import router as websocket_router
from app.logging_config import logger

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    # Initialize FastAPI app
    app = FastAPI(title="AI Tutor Chatbot API")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ALLOW_CREDENTIALS,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
    )
    
    # Include routers
    app.include_router(base_router)
    app.include_router(sessions_router)
    app.include_router(websocket_router)
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    return app

# Create the application instance
app = create_app()

def start():
    """Start the application with uvicorn"""
    logger.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD)

if __name__ == "__main__":
    start() 