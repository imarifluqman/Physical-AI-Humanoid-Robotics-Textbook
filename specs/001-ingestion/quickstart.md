# Quickstart: Book Content Ingestion Module

## Overview
Quickstart guide for setting up and running the book content ingestion module that converts documentation to vector embeddings for chatbot integration.

## Prerequisites

### System Requirements
- Python 3.11 or higher
- Git
- Access to Cohere API (with API key)
- Access to Qdrant database (URL and API key if required)

### Python Dependencies
The following Python packages will be installed:
- `qdrant-client`
- `cohere`
- `python-dotenv`
- `rich`
- `pytest` (for testing)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install qdrant-client cohere python-dotenv rich pytest
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following content:

```env
QDRANT_URL=<your_qdrant_url>
QDRANT_API_KEY=<your_qdrant_api_key_if_needed>
COHERE_API_KEY=<your_cohere_api_key>
FRONTEND_DOCS_PATH=../frontend/docs
```

**Note**: Never commit the `.env` file to version control. A `.env.example` file is provided as a template.

## Running the Ingestion Process

### 1. Verify Documentation Directory Structure
Ensure your documentation follows this structure:
```
../frontend/docs/
├── module1/
│   ├── chapter1.md
│   ├── chapter2.md
│   └── ...
├── module2/
│   ├── chapter1.md
│   ├── chapter2.md
│   └── ...
└── ...
```

### 2. Run the Ingestion Script
```bash
cd backend/src/ingestion
python main.py
```

### 3. Monitor Progress
The ingestion process will display progress using the `rich` library, showing:
- Which module and chapter are being processed
- Embedding generation status
- Upload progress to Qdrant
- Any errors or warnings

## Configuration Options

### Environment Variables
- `QDRANT_URL`: URL of your Qdrant instance (e.g., `https://your-cluster.qdrant.tech:6333`)
- `QDRANT_API_KEY`: API key for Qdrant authentication (if required)
- `COHERE_API_KEY`: API key for Cohere embedding service
- `FRONTEND_DOCS_PATH`: Path to the documentation directory (default: `../frontend/docs`)
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings (default: `book_embeddings`)
- `CHUNK_SIZE`: Maximum size of text chunks in tokens (default: 512)
- `BATCH_SIZE`: Number of embeddings to process in each batch (default: 10)

## Verification

### 1. Check Qdrant Collection
After ingestion completes, verify the data in Qdrant:
- Collection exists with the expected name
- Records contain proper metadata (module, chapter, text)
- Vector dimensions match expected size (1024 for embed-english-v3.0)

### 2. Test Similarity Search
You can test that embeddings work correctly by performing a simple similarity search against the Qdrant collection.

## Troubleshooting

### Common Issues

#### API Rate Limits
If you encounter rate limit errors:
- Implement retry logic with exponential backoff
- Reduce the number of concurrent requests
- Check your Cohere and Qdrant rate limits

#### Large File Errors
If large files cause issues:
- The system automatically chunks large files
- Verify chunk size configuration is appropriate
- Check memory usage during processing

#### Connection Issues
If unable to connect to Qdrant or Cohere:
- Verify API keys are correct
- Check network connectivity
- Ensure URLs are properly formatted

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

## Next Steps

1. After successful ingestion, the data is ready for the chatbot to perform semantic searches
2. Configure the chatbot to connect to the same Qdrant instance
3. Test the end-to-end functionality with sample queries