from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import time

from app.config import LLM_MODEL_NAME, SYSTEM_PROMPT
from app.logging_config import logger

# Initialize the LLM prompt template
CHAT_PROMPT = ChatPromptTemplate.from_template("""
{system_prompt}

Here is the conversation so far:
{history}

Now, answer the latest question:

Kid: {question}

Tutor:
""")

class LLMService:
    """Service for interacting with the LLM"""
    
    def __init__(self):
        """Initialize the LLM service"""
        self._model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LLM model"""
        try:
            self._model = OllamaLLM(model=LLM_MODEL_NAME)
            logger.info(f"Successfully initialized LLM model: {LLM_MODEL_NAME}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self._model = None
    
    async def generate_response(self, history: str, question: str) -> str:
        """Generate a response using the LLM"""
        if not self._model:
            logger.error("LLM model not initialized")
            return "I'm sorry, I'm having trouble thinking right now. Could you try again?"
        
        try:
            start_time = time.time()
            
            # Call LLM through LangChain
            chain = CHAT_PROMPT | self._model
            response = chain.invoke({
                "system_prompt": SYSTEM_PROMPT,
                "history": history,
                "question": question
            })
            
            # Process response
            reply = response.strip()
            
            # Log timing
            duration = time.time() - start_time
            logger.info(f"Generated response in {duration:.2f}s")
            
            return reply
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble thinking right now. Could you try again?"

# Initialize LLM service
llm_service = LLMService() 