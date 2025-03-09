# Private GPT - AI Tutor Chatbot

A multi-session, multi-user WebSocket-based chat application with AI tutoring capabilities.

## Features

- 🔄 Multi-session support - users can have multiple chat sessions
- 👥 Multi-user support - different users can use the application simultaneously
- 🔌 WebSocket-based real-time communication
- 🤖 Integration with LLaMA3.2 via Ollama
- 📊 Session management API
- 🏃 Auto-reconnection and connection management

## Project Structure

```
private-gpt/
├── app/
│   ├── __init__.py           # App initialization
│   ├── main.py               # Entry point
│   ├── config.py             # Configuration and settings
│   ├── logging_config.py     # Logging configuration
│   ├── models/               # Pydantic models
│   │   ├── __init__.py
│   │   └── schemas.py        # API request/response schemas
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── chat_session.py   # Chat session management
│   │   ├── session_manager.py # Multi-session management
│   │   └── llm_service.py    # LLM integration
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   ├── base.py           # Basic API routes
│   │   ├── sessions.py       # Session management routes
│   │   └── websocket.py      # WebSocket endpoints
└── templates/                # HTML templates
    └── chat.html
└── static/                   # Static files
```

## Setup and Installation

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```
   pip install fastapi uvicorn langchain_ollama langchain_core
   ```
3. Make sure you have Ollama installed and running with LLaMA3.2 model
   ```
   ollama pull llama3.2
   ```

## Running the Application

Run the application using the following command:

```bash
python -m app.main
```

The application will be available at:
- Web UI: http://localhost:8000/chat
- API: http://localhost:8000/

## API Endpoints

- `GET /` - Status information
- `POST /sessions` - Create a new session
- `GET /sessions/{user_id}` - Get all sessions for a user
- `PUT /sessions/{session_id}/title` - Update session title
- `DELETE /sessions/{session_id}` - Delete a session
- `GET /chat/{session_id}` - Get chat page for a specific session
- `GET /chat` - Create a new session and get its chat page
- WebSocket: `/chat/{session_id}` - WebSocket endpoint for chat sessions
- WebSocket: `/chatbot` - Legacy WebSocket endpoint (creates a new session) 