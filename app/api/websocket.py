from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from app.services.session_manager import session_manager
from app.services.llm_service import llm_service
from app.logging_config import logger

# Create router
router = APIRouter()

@router.websocket("/chat/{session_id}")
async def chat_websocket(websocket: WebSocket, session_id: str):
    """Main WebSocket endpoint for chat sessions"""
    session = None
    try:
        # Connect to session
        session = await session_manager.connect(websocket, session_id)

        # Send welcome message if this is a new session
        if len(session.messages) == 0:
            welcome_message = "Hello! I'm your AI tutor. What would you like to learn about today?"
            session.add_message("assistant", welcome_message)
            await websocket.send_text(welcome_message)

        # Process messages
        while True:
            # Wait for message from client
            data = await websocket.receive_text()

            # Add user message to history
            session.add_message("user", data)

            # Update session title if this is the first message
            if len(session.messages) == 2:  # Welcome + first user message
                # Extract first ~20 chars from first message
                title = data[:20] + ("..." if len(data) > 20 else "")
                session.update_title(title)

            # Generate response
            try:
                # Get formatted conversation history
                history = session.get_history_text()

                # Generate response using LLM service
                reply = await llm_service.generate_response(history, data)

                # Add assistant message to history
                session.add_message("assistant", reply)

                # Send response to client
                await websocket.send_text(reply)

            except Exception as e:
                logger.error(f"Error generating response: {e}")
                error_message = "I'm sorry, I'm having trouble thinking right now. Could you try again?"
                await websocket.send_text(error_message)
                session.add_message("assistant", error_message)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if session and session.is_connected():
            try:
                await session.active_connection.close()
            except:
                pass
    finally:
        # Clean up connection
        session_manager.disconnect(websocket)


@router.websocket("/chatbot")
async def legacy_chatbot_websocket(websocket: WebSocket):
    """Legacy WebSocket endpoint for backward compatibility"""
    # Create a new session
    session = session_manager.create_session()

    # Redirect to the new endpoint
    await chat_websocket(websocket, session.session_id) 