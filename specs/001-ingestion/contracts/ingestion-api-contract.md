# Ingestion Module API Contract

## Overview
This document defines the interface contract for the book content ingestion module that converts documentation to vector embeddings for chatbot integration.

## Configuration Interface

### Environment Variables
The ingestion module requires the following environment variables:

```
QDRANT_URL: string (required)
  - Description: URL for the Qdrant vector database
  - Format: Valid HTTP/HTTPS URL
  - Example: "https://your-cluster.qdrant.tech:6333"

QDRANT_API_KEY: string (optional)
  - Description: API key for Qdrant authentication
  - Format: String token
  - Example: "your-api-key-here"

COHERE_API_KEY: string (required)
  - Description: API key for Cohere embedding service
  - Format: String token
  - Example: "your-cohere-api-key-here"

FRONTEND_DOCS_PATH: string (required)
  - Description: Path to the documentation directory
  - Format: File system path
  - Example: "../frontend/docs"

QDRANT_COLLECTION_NAME: string (optional)
  - Description: Name of the Qdrant collection to store embeddings
  - Default: "book_embeddings"
  - Format: Valid collection name

CHUNK_SIZE: integer (optional)
  - Description: Maximum size of text chunks in tokens
  - Default: 512
  - Format: Positive integer
  - Range: 100-1000

BATCH_SIZE: integer (optional)
  - Description: Number of embeddings to process in each batch
  - Default: 10
  - Format: Positive integer
  - Range: 1-100
```

## Functional Interface

### Main Execution
The ingestion module provides a command-line interface through the main execution:

```
Input: None (reads configuration from environment variables)
Output: Status messages and completion indicator
Exit Codes:
  0: Success - all content ingested successfully
  1: General error - configuration issue or processing error
  2: Connection error - unable to connect to APIs
  3: Data error - issues with source files or processing
```

## Data Interface

### Input Data Format
The ingestion module expects documentation in the following directory structure:

```
{FRONTEND_DOCS_PATH}/
├── module{N}/
│   ├── chapter{M}.md
│   └── ...
└── ...
```

Where:
- `{N}` and `{M}` are numeric identifiers
- `.md` files contain markdown-formatted text content

### Output Data Format
The module stores embedding records in Qdrant with the following structure:

```
{
  "id": string (UUID),
  "vector": array of floats,
  "payload": {
    "text": string,
    "module": string,
    "chapter": string,
    "chunk_index": integer (optional),
    "source_file": string
  }
}
```

## Error Interface

### Error Handling
The ingestion module follows these error handling patterns:

1. **Configuration Errors**: Fail fast with descriptive error message
2. **File Access Errors**: Log error and continue with remaining files
3. **API Errors**: Retry with exponential backoff up to 3 attempts
4. **Database Errors**: Log error and continue with remaining items

### Logging Interface
The module outputs progress information using the rich library formatting:

```
Progress: Module X/Y, Chapter A/B - Processing
Status: Embedding generation complete for chapter Z
Success: Uploaded N embeddings to Qdrant
Error: Failed to process file path - reason
```

## Performance Interface

### Expected Performance
The module should process:
- 4 modules with 10 chapters each within 30 minutes
- Handle files up to 10MB in size
- Respect API rate limits without manual intervention