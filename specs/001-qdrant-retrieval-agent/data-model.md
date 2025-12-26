# Data Model: Qdrant Retrieval Agent

## Entities

### Query
**Description**: Natural language text input from user seeking information about book content
**Fields**:
- `query_text` (string, required): The user's natural language query (max 1000 characters)
- `user_id` (string, optional): Identifier for the requesting user
- `timestamp` (datetime, required): When the query was submitted
- `context` (string, optional): Additional context for the query

**Validation Rules**:
- Query text must be 1-1000 characters
- Query text must not be empty or whitespace-only
- User ID must follow UUID format if provided

### Retrieved Content
**Description**: Text snippets from the Physical AI & Humanoid Robotics book with associated metadata
**Fields**:
- `content_id` (string, required): Unique identifier for the content snippet
- `text_content` (string, required): The actual text content retrieved
- `module` (string, required): Module identifier (e.g., "module1", "module2")
- `chapter` (string, required): Chapter identifier (e.g., "chapter1", "chapter3")
- `section` (string, optional): Section name within the chapter
- `similarity_score` (float, required): Similarity score from vector search (0.0-1.0)
- `metadata` (object, optional): Additional metadata associated with the content

**Validation Rules**:
- Text content must not be empty
- Module and chapter must be valid identifiers
- Similarity score must be between 0.0 and 1.0
- Content ID must be unique

### Agent Response
**Description**: AI-generated answer based on retrieved content, providing information to the user
**Fields**:
- `response_id` (string, required): Unique identifier for the response
- `query_id` (string, required): Reference to the original query
- `answer` (string, required): The AI-generated answer
- `retrieved_content` (array[Retrieved Content], required): Content used to generate the answer
- `confidence` (float, optional): Confidence score of the response (0.0-1.0)
- `timestamp` (datetime, required): When the response was generated
- `source_modules` (array[string], required): List of modules referenced in the response

**Validation Rules**:
- Answer must not be empty
- Must reference at least one retrieved content item
- Confidence score must be between 0.0 and 1.0 if provided
- Source modules must be valid module identifiers

### Qdrant Record
**Description**: Vector representation of book content with metadata for semantic search and retrieval
**Fields**:
- `id` (string, required): Unique identifier for the record in Qdrant
- `vector` (array[float], required): The embedding vector
- `payload` (object, required): Metadata object containing:
  - `text_content` (string, required): Original text content
  - `module` (string, required): Module identifier
  - `chapter` (string, required): Chapter identifier
  - `section` (string, optional): Section name
  - `source_file` (string, optional): Original source file name
- `created_at` (datetime, required): When the record was created

**Validation Rules**:
- Vector must have consistent dimensionality
- Payload must contain required metadata fields
- ID must be unique within the collection

## Relationships

### Query → Agent Response
- One-to-one relationship (each query generates one response)
- Agent Response references Query via `query_id`

### Agent Response → Retrieved Content
- One-to-many relationship (one response can reference multiple content snippets)
- Agent Response contains array of Retrieved Content items

### Retrieved Content → Qdrant Record
- One-to-one relationship (each retrieved content corresponds to one Qdrant record)
- Retrieved Content is derived from Qdrant Record during search

## State Transitions

### Query States
1. **PENDING**: Query received, waiting for processing
2. **PROCESSING**: Query being processed by the AI agent
3. **COMPLETED**: Response successfully generated
4. **FAILED**: Error occurred during processing

### Agent Response States
1. **DRAFT**: Response being constructed
2. **VALIDATED**: Response validated against retrieved content (no hallucinations)
3. **READY**: Response ready to be returned to user
4. **ERROR**: Error occurred during response generation