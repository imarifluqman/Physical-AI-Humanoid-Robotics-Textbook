"""
Data models for the book content ingestion system.
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class EmbeddingRecord:
    """
    Represents a vector embedding of book content with associated metadata.
    """
    id: str  # UUID string
    vector: List[float]  # The vector embedding
    text: str  # The original text content
    module: str  # Module identifier (e.g., "module1", "module2")
    chapter: str  # Chapter identifier (e.g., "chapter1", "chapter2")
    chunk_index: Optional[int] = None  # Index if the original text was split
    created_at: datetime = None  # When this record was created
    source_file: str = ""  # Path to the original source file

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.id is None or self.id == "":
            self.id = str(uuid.uuid4())


@dataclass
class ProcessingStatus:
    """
    Tracks the progress and status of the ingestion process.
    """
    module: str
    chapter: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: float = 0.0  # Progress percentage (0.0 to 1.0)
    message: Optional[str] = None  # Additional status information
    timestamp: datetime = None  # When this status was recorded

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class Chunk:
    """
    Represents a chunk of text that will be converted to an embedding.
    """
    text: str
    module: str
    chapter: str
    chunk_index: int
    source_file: str