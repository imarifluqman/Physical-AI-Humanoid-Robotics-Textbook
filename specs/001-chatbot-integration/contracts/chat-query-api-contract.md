# API Contract: Chatbot Query Endpoint

## Endpoint
`POST /api/v1/query`

## Purpose
Submit a user query and receive an AI-generated response based on documentation content.

## Request Format

### HTTP Method
`POST`

### URL
`http://localhost:8000/api/v1/query`

### Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "messages": [
    {
      "role": "user",
      "content": "string (required) - The user's question or query"
    }
  ]
}
```

## Response Format

### Success Response (200 OK)
```json
{
  "role": "assistant",
  "content": "string - The AI-generated response to the user's query"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "error": "string - Description of the validation error"
}
```

#### 500 Internal Server Error
```json
{
  "error": "string - Description of the server error"
}
```

#### 503 Service Unavailable
```json
{
  "error": "string - Service temporarily unavailable"
}
```

## Validation Rules
- Request body must contain "messages" array
- Messages array must contain at least one message
- Each message must have "role" and "content" fields
- Message role must be "user" for input messages

## Example Request
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I configure authentication in this system?"
    }
  ]
}
```

## Example Response
```json
{
  "role": "assistant",
  "content": "To configure authentication, you need to set up the authentication provider in the configuration file..."
}
```