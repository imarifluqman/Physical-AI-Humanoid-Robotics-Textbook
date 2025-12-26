import logging
import os
from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging configuration
def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": "app.log",
                "mode": "a"
            }
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False
            },
            "agent": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console", "file"]
        }
    }

    dictConfig(logging_config)


# Set up logging
setup_logging()

# Create FastAPI app instance
app = FastAPI(
    title="Qdrant Retrieval Agent API",
    description="API for querying Physical AI & Humanoid Robotics book content using AI-powered semantic search",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json"  # OpenAPI schema
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routes
from .api.retrieval_endpoints import router as retrieval_router
app.include_router(retrieval_router, prefix="/api/v1", tags=["retrieval"])

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "qdrant-retrieval-agent"}

# For running the application directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )