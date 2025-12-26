import os
from dotenv import load_dotenv

load_dotenv()

# Qdrant Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Try OpenRouter as fallback
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        raise ValueError("Either OPENAI_API_KEY or OPENROUTER_API_KEY must be set in env file")

# Model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")  # Default model

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Application Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validation Configuration
MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", 1000))
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", 5))
