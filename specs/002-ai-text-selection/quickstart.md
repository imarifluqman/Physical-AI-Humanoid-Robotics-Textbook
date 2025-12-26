# Quickstart Guide: Contextual AI Assistant via Text Selection

## Overview
This guide provides a quick setup for developers to understand and implement the text selection to AI assistant feature.

## Prerequisites
- Node.js and npm installed
- Docusaurus project with existing chatbot component
- Basic knowledge of React and JavaScript

## Getting Started

### 1. File Structure
First, create the necessary directory and files:
```
src/
├── components/
│   └── ContextualAI/
│       ├── ContextualAIProvider.jsx
│       ├── SelectionActionButton.jsx
│       ├── useTextSelection.js
│       └── styles.css
```

### 2. Core Implementation Steps

#### Step 1: Create the text selection hook
Create `useTextSelection.js` with event listeners for detecting text selection:
- Use `window.getSelection()` to get selected text
- Listen for `mouseup` and `selectionchange` events
- Calculate position using `getBoundingClientRect()`

#### Step 2: Create the AI action button
Create `SelectionActionButton.jsx`:
- Position the button near the selection
- Style appropriately with CSS
- Handle click events to trigger chatbot

#### Step 3: Create the provider component
Create `ContextualAIProvider.jsx`:
- Wrap your main layout with this provider
- Manage global state for selection
- Coordinate between selection detection and button display

#### Step 4: Integrate with existing chatbot
- Access chatbot input through ref or context
- Inject selected text into chatbot input
- Ensure chatbot is opened when button is clicked

### 3. Key API Integration Points
- `window.getSelection()` - Get user's text selection
- `Range.getBoundingClientRect()` - Get position of selection
- Chatbot input setter method - Inject text into chatbot
- Event listener cleanup - Prevent memory leaks

### 4. Testing
- Select text on any page and verify button appears
- Click button and verify text is injected into chatbot
- Test on different page layouts and content types
- Verify accessibility features work with keyboard navigation

## Common Issues & Solutions

### Button positioning issues
- Ensure viewport boundary checks are implemented
- Use CSS transforms for precise positioning

### Event listener conflicts
- Implement proper cleanup in useEffect
- Use event listener options like `{ passive: true }`

### Chatbot integration problems
- Verify the chatbot exposes an input setter method
- Check that the chatbot state is preserved when injecting text

## Next Steps
After completing the basic implementation, consider:
- Adding accessibility features
- Implementing mobile support
- Adding analytics to track usage