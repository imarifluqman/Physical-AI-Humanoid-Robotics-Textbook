import React, { useEffect, useRef } from 'react';
import './styles.css';

/**
 * SelectionActionButton component
 * Displays the AI assistant button near the selected text
 */
const SelectionActionButton = ({ selectedText, position, isVisible, onAskAI }) => {
  const buttonRef = useRef(null);

  // Update button position when it becomes visible or when position changes
  useEffect(() => {
    if (buttonRef.current) {
      if (isVisible && position) {
        const button = buttonRef.current;
        // Calculate position, ensuring it stays within viewport bounds
        let topPos = position.y - 50; // Position above the selection
        let leftPos = position.x;

        // Ensure button stays within viewport
        const buttonHeight = 100;
        const buttonWidth = 100;
        const viewportHeight = window.innerHeight;
        const viewportWidth = window.innerWidth;

        // Adjust top position if button would be above viewport
        if (topPos < 0) {
          topPos = position.y + 20; // Position below selection if above viewport
        }

        // Adjust if button would be below viewport (but still make sure it's positioned relative to the actual text)
        if (topPos + buttonHeight > window.scrollY + viewportHeight) {
          topPos = position.y - buttonHeight - 5; // Position above selection
        }

        // If the selected text is far down the page, make sure the button is still visible in current viewport
        if (position.y < window.scrollY) {
          // Selected text is above the current viewport, position button below current viewport top
          topPos = window.scrollY + 10;
        } else if (position.y > window.scrollY + viewportHeight) {
          // Selected text is below current viewport, position button above current viewport bottom
          topPos = window.scrollY + viewportHeight - buttonHeight - 10;
        }

        // Adjust left position if button would be outside viewport
        if (leftPos + buttonWidth > viewportWidth) {
          leftPos = viewportWidth - buttonWidth - 10; // Position within right edge
        }

        if (leftPos < 0) {
          leftPos = 10; // Position within left edge
        }

        // Position the button near the selection, ensuring it doesn't block the text
        button.style.top = `${topPos}px`;
        button.style.left = `${leftPos}px`;

        // Add visible class to show the button
        button.classList.add('visible');
      } else {
        // Remove visible class to hide the button
        buttonRef.current.classList.remove('visible');
      }
    }
  }, [position, isVisible]); // Include position in dependency array to update on position changes

  // Handle button click to trigger chatbot opening and text injection
  const handleClick = () => {
    if (onAskAI) {
      onAskAI(selectedText);
    }
  };

  if (!isVisible || !selectedText || !position) {
    return null;
  }

  return (
    <button
      ref={buttonRef}
      className="contextual-ai-button"
      onClick={handleClick}
      aria-label="Ask AI about selected text"
      aria-describedby="contextual-ai-description"
      role="button"
      title="Ask AI about selected text"
    >
      <span className="contextual-ai-button-icon" aria-hidden="true">Ask</span>
      <span id="contextual-ai-description" style={{ display: 'none' }}>
        Click to ask AI assistant about the selected text
      </span>
    </button>
  );
};

export default SelectionActionButton;