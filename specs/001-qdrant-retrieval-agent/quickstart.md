# Quickstart Guide: Qdrant Retrieval Agent

## Overview
This guide provides instructions to quickly set up and run the Qdrant Retrieval Agent for querying Physical AI & Humanoid Robotics book content.

## Prerequisites
- Python 3.11+
- Qdrant vector database running (local or remote)
- Google AI API key for Gemini model access
- (Optional) Anthropic API key for Claude model access

## Installation

### 1. Clone the repository
```bash
git clone [repository-url]
cd [repository-name]
```

### 2. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root with the following variables:

```env
# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=book_content

# AI Model Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL_NAME=gemini-pro  # or another supported model

# Optional: Anthropic Configuration
ANTHROPIC_API_KEY=your-anthropic-api-key

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Running the Service

### 1. Start Qdrant
If running locally:
```bash
docker run -p 6333:6333 -v ./qdrant_storage:/qdrant/storage qdrant/qdrant
```

### 2. Start the API server
```bash
cd backend
python src/main.py
```

The API will be available at `http://localhost:8000`

## Usage Examples

### Query the API
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key principles of humanoid locomotion?"
  }'
```

### Expected Response
```json
{
  "response_id": "resp-67890",
  "query": "What are the key principles of humanoid locomotion?",
  "answer": "The key principles of humanoid locomotion include dynamic balance control, bipedal gait patterns, and compliant joint actuation...",
  "retrieved_content": [
    {
      "content_id": "content-abc123",
      "text_content": "Humanoid locomotion requires dynamic balance control through feedback systems...",
      "module": "module3",
      "chapter": "chapter5",
      "section": "balance_control_principles",
      "similarity_score": 0.92,
      "metadata": {
        "page_number": 145,
        "keywords": ["balance", "locomotion", "feedback"]
      }
    }
  ],
  "confidence": 0.85,
  "source_modules": ["module3"],
  "timestamp": "2025-12-18T10:30:00Z"
}
```

## Testing the Health Endpoint
```bash
curl http://localhost:8000/api/v1/health
```

## Development

### Running Tests
```bash
cd backend
python -m pytest tests/
```

### Running Specific Test Types
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Contract tests
python -m pytest tests/contract/
```

## Troubleshooting

### Common Issues
1. **Qdrant Connection Error**: Verify Qdrant is running and accessible at the configured host/port
2. **API Key Issues**: Check that your API keys are valid and have the necessary permissions
3. **No Results Returned**: Verify that book content has been ingested into Qdrant

### Debugging
Enable debug logging by setting the environment variable:
```env
LOG_LEVEL=DEBUG
```