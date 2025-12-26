"""
Ingestion module for the book content ingestion system.
"""
__version__ = "0.1.0"
__author__ = "Book Ingestion Team"

# Import main components for easy access
from .config import Config, load_config, validate_config
from .models import EmbeddingRecord, ProcessingStatus, Chunk
from .reader import FileReader
from .embedder import CohereEmbedder
from .uploader import QdrantUploader
from .chunker import TextChunker
from .logging import logger, IngestionLogger

__all__ = [
    "Config",
    "load_config",
    "validate_config",
    "EmbeddingRecord",
    "ProcessingStatus",
    "Chunk",
    "FileReader",
    "CohereEmbedder",
    "QdrantUploader",
    "TextChunker",
    "logger",
    "IngestionLogger"
]