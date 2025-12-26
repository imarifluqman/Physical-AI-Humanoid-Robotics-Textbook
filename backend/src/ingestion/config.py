"""
Configuration module for the book content ingestion system.
Handles environment variables and validation.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
@dataclass
class Config:
    """
    Configuration for the ingestion process.
    """
    qdrant_url: str
    qdrant_api_key: Optional[str]
    cohere_api_key: str
    frontend_docs_path: str
    collection_name: str = "book_embeddings"
    chunk_size: int = 512  # tokens
    batch_size: int = 10
    retry_attempts: int = 3


def load_config() -> Config:
    """
    Load configuration from environment variables.

    Returns:
        Config: Validated configuration object

    Raises:
        ValueError: If required environment variables are missing
    """
    qdrant_url = os.getenv("QDRANT_URL")
    if not qdrant_url:
        raise ValueError("QDRANT_URL environment variable is required")

    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    frontend_docs_path = os.getenv("FRONTEND_DOCS_PATH", "../frontend/docs")

    # Validate that the docs path exists
    if not os.path.exists(frontend_docs_path):
        raise ValueError(f"FRONTEND_DOCS_PATH does not exist: {frontend_docs_path}")

    return Config(
        qdrant_url=qdrant_url,
        qdrant_api_key=os.getenv("QDRANT_API_KEY"),
        cohere_api_key=cohere_api_key,
        frontend_docs_path=frontend_docs_path,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME", "book_embeddings"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "512")),
        batch_size=int(os.getenv("BATCH_SIZE", "10")),
        retry_attempts=int(os.getenv("RETRY_ATTEMPTS", "3"))
    )


def validate_config(config: Config) -> None:
    """
    Validate the configuration values.

    Args:
        config: Configuration to validate

    Raises:
        ValueError: If configuration values are invalid
    """
    if not config.qdrant_url.startswith(("http://", "https://")):
        raise ValueError(f"QDRANT_URL must be a valid URL: {config.qdrant_url}")

    if config.chunk_size <= 0:
        raise ValueError(f"CHUNK_SIZE must be positive: {config.chunk_size}")

    if config.batch_size <= 0:
        raise ValueError(f"BATCH_SIZE must be positive: {config.batch_size}")

    if config.retry_attempts <= 0:
        raise ValueError(f"RETRY_ATTEMPTS must be positive: {config.retry_attempts}")

    if not os.path.exists(config.frontend_docs_path):
        raise ValueError(f"FRONTEND_DOCS_PATH does not exist: {config.frontend_docs_path}")