# Data Model: Contextual AI Assistant via Text Selection

## Core Entities

### SelectedText
- **Definition**: The content that the user has highlighted on the page
- **Attributes**:
  - `text`: string (the actual selected text content)
  - `range`: Range object (DOM range of the selection)
  - `boundingRect`: DOMRect (position and dimensions of the selection)
  - `timestamp`: number (when the selection was made)
- **Validation**:
  - Must not be empty or whitespace-only
  - Length should be reasonable (e.g., less than 10,000 characters)
- **Relationships**: Belongs to a single SelectionAction

### SelectionAction
- **Definition**: The user action of selecting text and triggering the AI assistant
- **Attributes**:
  - `id`: string (unique identifier for the action)
  - `selectedText`: SelectedText (the text that was selected)
  - `position`: object (coordinates for button positioning)
  - `status`: enum ('active', 'completed', 'cancelled')
- **State transitions**:
  - 'active' when text is selected
  - 'completed' when button is clicked
  - 'cancelled' when selection is cleared
- **Relationships**: Contains one SelectedText

### AIActionButton
- **Definition**: The UI element that appears near selected text
- **Attributes**:
  - `id`: string (unique identifier)
  - `position`: object (x, y coordinates relative to viewport)
  - `isVisible`: boolean (whether button is currently displayed)
  - `element`: HTMLElement (the actual DOM element)
- **Validation**:
  - Must not overlap with selected text
  - Must be positioned within viewport boundaries
- **Relationships**: Associated with one SelectionAction

## State Flow

1. User selects text → SelectedText entity created
2. System detects selection → SelectionAction entity created with 'active' status
3. Button appears → AIActionButton entity created with 'isVisible' = true
4. User clicks button → SelectedText injected into chatbot input
5. Selection cleared → SelectionAction status changes to 'cancelled', button hidden

## Constraints

- SelectedText length: Maximum 10,000 characters to prevent performance issues
- Button positioning: Must maintain at least 10px distance from selected text edges
- Memory management: Entities must be cleaned up when no longer needed
- Accessibility: All entities must support keyboard navigation and screen readers