# Chatbot Component Documentation

## Overview
The Chatbot component provides a conversational interface for users to query documentation using natural language. The component integrates with a backend API to provide AI-generated responses based on documentation content.

## Components

### Chatbot
The main chat interface component that manages the conversation flow.

#### Usage
```jsx
import { Chatbot } from './components/Chatbot';

function App() {
  return (
    <div>
      <Chatbot />
    </div>
  );
}
```

#### Features
- Real-time conversation interface
- Message history management
- Loading states
- Error handling
- Accessibility support

### FloatingChatWidget
A floating widget implementation that can be integrated into any page layout.

#### Usage
```jsx
import { FloatingChatWidget } from './components/Chatbot';

function App() {
  return (
    <div>
      {/* Your main content */}
      <FloatingChatWidget />
    </div>
  );
}
```

## API Integration
The component communicates with the backend API at `http://localhost:8000/api/v1/query` using the POST method. The API should accept a JSON payload with a `messages` array containing message objects with `role` and `content` properties.

## Configuration
The component uses the following default configuration:
- API Base URL: `http://localhost:8000`
- Message display format: Chronological order with role-based styling
- Error handling: Graceful degradation with user-friendly messages

## Accessibility
The component includes the following accessibility features:
- ARIA labels for screen readers
- Keyboard navigation support
- Proper semantic HTML structure
- Focus management

## Performance
The components use React.memo for performance optimization to prevent unnecessary re-renders.

## Error Handling
- Network error detection
- User-friendly error messages
- Graceful degradation when backend is unavailable
- Prevents UI crashes during error conditions