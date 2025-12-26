from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class QueryRequest(BaseModel):
    """
    Model for the query request from users
    """
    query: str
    user_id: Optional[str] = None
    timestamp: datetime = datetime.now()
    context: Optional[str] = None

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty or whitespace only')
        if len(v) > 1000:
            raise ValueError('Query exceeds maximum length of 1000 characters')
        return v.strip()


class RetrievedContent(BaseModel):
    """
    Model for content retrieved from Qdrant
    """
    content_id: str
    text_content: str
    module: str
    chapter: str
    section: Optional[str] = None
    similarity_score: float
    metadata: Optional[Dict[str, Any]] = {}


class QueryResponse(BaseModel):
    """
    Model for the response to user queries
    """
    response_id: str
    query: str
    answer: str
    retrieved_content: List[RetrievedContent]
    confidence: Optional[float] = None
    timestamp: datetime = datetime.now()
    source_modules: List[str]


class ErrorResponse(BaseModel):
    """
    Model for error responses
    """
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = {}


class HealthResponse(BaseModel):
    """
    Model for health check responses
    """
    status: str
    timestamp: datetime = datetime.now()
    details: Optional[Dict[str, Any]] = {}