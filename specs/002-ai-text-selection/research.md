# Research Notes: Contextual AI Assistant via Text Selection

## Decision: Text Selection Detection Method
**Rationale**: Using `window.getSelection()` is the standard browser API for detecting text selection. Combined with `mouseup` and `selectionchange` events, it provides reliable detection of user text selection without interfering with native behavior.

**Alternatives considered**:
- MutationObserver: More complex and not necessary for text selection
- Custom selection tracking: Would require more complex implementation

## Decision: Button Positioning Strategy
**Rationale**: Using `Range.getBoundingClientRect()` provides accurate positioning relative to the selected text. This ensures the button appears near the selection without blocking the text.

**Alternatives considered**:
- Static positioning: Would not be contextual
- CSS-based positioning: Less accurate for text selections

## Decision: Integration Method with Docusaurus
**Rationale**: The Docusaurus Layout component is the ideal place to mount global event listeners as it's present on all pages. This ensures consistent behavior across the entire documentation site.

**Alternatives considered**:
- Individual page components: Would require duplication
- Custom wrapper: Unnecessary complexity

## Decision: Chatbot Integration Approach
**Rationale**: Using React's ref system or context API to access the chatbot's input setter provides a clean separation while allowing text injection without modifying the chatbot internals.

**Alternatives considered**:
- Direct DOM manipulation: Less maintainable
- Global event system: More complex than needed

## Decision: Event Listener Management
**Rationale**: Using React's useEffect hook with proper cleanup ensures no memory leaks occur and event listeners are properly removed when components unmount.

**Alternatives considered**:
- Global event handlers: Risk of memory leaks
- Manual cleanup: Error-prone

## Decision: Accessibility Implementation
**Rationale**: Following WCAG guidelines for focus management and ARIA attributes ensures the feature is accessible to all users, including those using screen readers.

**Alternatives considered**:
- Minimal accessibility: Would exclude users with disabilities