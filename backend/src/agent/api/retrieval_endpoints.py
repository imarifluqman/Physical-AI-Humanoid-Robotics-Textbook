from fastapi import APIRouter, HTTPException, status, Request
import logging
from typing import Optional
from ..models.query_models import QueryRequest, QueryResponse, ErrorResponse, HealthResponse
from ..services.retrieval_agent import retrieval_agent
from ..exceptions import AgentProcessingException, ContentRetrievalException, QueryValidationException
from ..config import LOG_LEVEL

logger = logging.getLogger("agent")

# Simple in-memory rate limiting (in production, use redis or similar)
request_counts = {}
RATE_LIMIT = 10  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

router = APIRouter()

def check_rate_limit(client_ip: str) -> bool:
    """
    Simple rate limiting function to limit requests per IP
    """
    import time
    current_time = time.time()

    # Clean up old entries
    keys_to_remove = []
    for ip, (count, timestamp) in request_counts.items():
        if current_time - timestamp > RATE_LIMIT_WINDOW:
            keys_to_remove.append(ip)

    for ip in keys_to_remove:
        del request_counts[ip]

    # Check if client has exceeded rate limit
    if client_ip in request_counts:
        count, timestamp = request_counts[client_ip]
        if current_time - timestamp < RATE_LIMIT_WINDOW and count >= RATE_LIMIT:
            return False  # Rate limit exceeded
        else:
            request_counts[client_ip] = (count + 1, current_time)
    else:
        request_counts[client_ip] = (1, current_time)

    return True

@router.post("/query", response_model=QueryResponse, summary="Submit a natural language query")
async def query_endpoint(request: QueryRequest, req: Request):
    """
    Submit a natural language query about book content and receive an AI-generated response
    with relevant content snippets.
    """
    # Get client IP for rate limiting
    client_ip = req.client.host if req.client else "unknown"

    # Check rate limit
    if not check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error_code": "RATE_LIMIT_EXCEEDED",
                "message": f"Rate limit exceeded. Maximum {RATE_LIMIT} requests per minute."
            }
        )

    try:
        logger.info(f"Received query from {client_ip}: {request.query[:50]}...")  # Log first 50 chars

        # Process the query through the retrieval agent
        response = await retrieval_agent.process_query(request)

        logger.info(f"Successfully processed query from {client_ip}, returning response with ID: {response.response_id}")
        logger.debug(f"Response details - Answer length: {len(response.answer)}, Retrieved content count: {len(response.retrieved_content)}, Confidence: {response.confidence}")

        return response

    except QueryValidationException as e:
        logger.error(f"Query validation error from {client_ip}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": e.error_code,
                "message": e.message
            }
        )
    except ContentRetrievalException as e:
        logger.error(f"Content retrieval error from {client_ip}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_code": e.error_code,
                "message": e.message
            }
        )
    except AgentProcessingException as e:
        logger.error(f"Agent processing error from {client_ip}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": e.error_code,
                "message": e.message
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error processing query from {client_ip}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "UNEXPECTED_ERROR",
                "message": "An unexpected error occurred while processing the query"
            }
        )


@router.get("/health", response_model=HealthResponse, summary="Check API health status")
async def health_endpoint():
    """
    Check the health status of the retrieval agent service
    """
    try:
        # In a real implementation, you might want to check if Qdrant is accessible
        # For now, we'll just return a healthy status
        from ..services.qdrant_service import qdrant_service
        qdrant_healthy = qdrant_service.check_connection()

        health_status = "healthy" if qdrant_healthy else "unhealthy"

        response = HealthResponse(
            status=health_status
        )

        logger.info(f"Health check completed, status: {health_status}")
        return response

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            details={"error": str(e)}
        )


@router.get("/", summary="API root endpoint")
async def root():
    """
    Root endpoint for the retrieval API
    """
    return {"message": "Qdrant Retrieval Agent API", "status": "running"}