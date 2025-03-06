from fastapi import FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """You are a friendly and patient AI tutor who helps kids with their daily study doubts.

When answering, always:
- Explain concepts in a **simple and engaging way**.
- Use **examples** or **stories** when helpful.
- Keep explanations **short and to the point**.
- If needed, ask **follow-up questions** to guide the child.

Now, answer the question below:

Kid: {question}

Tutor:"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.2")

chain = prompt | model

chain.invoke({"question": "What is LangChain?"})

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


class ConnectionManager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

active_connections = {}


@app.websocket("/chatbot")  # Changed WebSocket endpoint
async def chatbot_websocket(websocket: WebSocket):
    client_id = websocket.client  # Unique client tracking

    # Ensure only one connection per client
    if client_id in active_connections:
        await websocket.close()
        return

    await websocket.accept()
    active_connections[client_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            print(f"User: {data}")

            # Call LangChain pipeline
            response = chain.invoke({"question": data})
            reply = response.strip()  # Ensure clean response
            print(f"Ollama: {reply}")

            await websocket.send_text(reply)  # Send response back

    except WebSocketDisconnect:
        del active_connections[client_id]
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
        active_connections.pop(client_id, None)

@app.get("/chat")
def get():
    with open("chat.html", "r") as file:
        return HTMLResponse(content=file.read())
