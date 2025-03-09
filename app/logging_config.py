import logging

def configure_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    
    # Create logger
    logger = logging.getLogger("chatbot")
    return logger

# Create and configure the logger
logger = configure_logging() 