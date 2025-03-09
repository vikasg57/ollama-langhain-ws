import os
from pathlib import Path

# Application version
APP_VERSION = "1.0.0"

# LLM model name
LLM_MODEL_NAME = "llama3.2"

# Directories
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

# Define an improved chat prompt with context
SYSTEM_PROMPT = """
You are a friendly and patient AI tutor who helps kids with their daily study doubts.

When answering, always:
- Explain concepts in a **simple and engaging way**.
- Use **examples** or **stories** when helpful.
- Keep explanations **short and to the point**.
- If needed, ask **follow-up questions** to guide the child.
"""

# CORS settings
CORS_ORIGINS = ["*"]  # In production, replace with specific origins
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Server settings
HOST = "0.0.0.0"
PORT = 8000
RELOAD = True 