"""
Custom exceptions for the Qdrant Retrieval Agent
"""


class AgentException(Exception):
    """
    Base exception class for the retrieval agent
    """
    def __init__(self, message: str, error_code: str = "AGENT_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class QdrantConnectionException(AgentException):
    """
    Exception raised when there are issues connecting to Qdrant
    """
    def __init__(self, message: str = "Failed to connect to Qdrant database"):
        super().__init__(message, "QDRANT_CONNECTION_ERROR")


class QueryValidationException(AgentException):
    """
    Exception raised when query validation fails
    """
    def __init__(self, message: str = "Query validation failed"):
        super().__init__(message, "QUERY_VALIDATION_ERROR")


class ContentRetrievalException(AgentException):
    """
    Exception raised when content retrieval fails
    """
    def __init__(self, message: str = "Failed to retrieve content from Qdrant"):
        super().__init__(message, "CONTENT_RETRIEVAL_ERROR")


class AgentProcessingException(AgentException):
    """
    Exception raised when the AI agent processing fails
    """
    def __init__(self, message: str = "AI agent processing failed"):
        super().__init__(message, "AGENT_PROCESSING_ERROR")


class ConfigurationException(AgentException):
    """
    Exception raised when there are configuration issues
    """
    def __init__(self, message: str = "Configuration error"):
        super().__init__(message, "CONFIGURATION_ERROR")