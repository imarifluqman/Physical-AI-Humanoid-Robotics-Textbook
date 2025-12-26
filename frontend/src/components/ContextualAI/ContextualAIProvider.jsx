import React, { useEffect, useRef } from 'react';
import { useTextSelection } from './useTextSelection';
import SelectionActionButton from './SelectionActionButton';
import { getGlobalChatbotRef } from './GlobalChatbotRef';

/**
 * ContextualAIProvider component
 * Provides the context for the contextual AI assistant feature
 * Monitors text selection and displays the AI button when text is selected
 */
const ContextualAIProvider = ({ children }) => {
  const containerRef = useRef(null);
  const { selectedText, selectionPosition, isVisible, hideButton } = useTextSelection();

  // Handle click outside to hide button
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        hideButton();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [hideButton]);

  // Function to handle asking AI with selected text
  const handleAskAI = (text) => {
    // Get the global chatbot reference
    const chatbotRef = getGlobalChatbotRef();

    if (chatbotRef) {
      // Open the chat if it's not already open
      chatbotRef.openChat();
      // Inject the selected text into the chat input
      chatbotRef.setInputValue(text);
      // Focus the input for easy editing
      chatbotRef.focusInput();

      // Position cursor at the end of the injected text for easy editing
      setTimeout(() => {
        const chatInput = document.querySelector('textarea[aria-label="Chat message input"]');
        if (chatInput) {
          // Set cursor position to the end of the text
          chatInput.selectionStart = chatInput.value.length;
          chatInput.selectionEnd = chatInput.value.length;
        }
      }, 100);
    } else {
      // Fallback: try to find the chat widget in the DOM
      const fabButton = document.querySelector('.fab[aria-label="Open documentation chat"]');
      if (fabButton) {
        // Click the floating action button to open the chat
        fabButton.click();

        // Set the text after a short delay to allow the chat to open
        setTimeout(() => {
          const chatInput = document.querySelector('textarea[aria-label="Chat message input"]');
          if (chatInput) {
            chatInput.value = text;
            // Trigger input event to update React state
            const event = new Event('input', { bubbles: true });
            chatInput.dispatchEvent(event);

            // Focus the input
            chatInput.focus();

            // Position cursor at the end of the text for easy editing
            chatInput.selectionStart = chatInput.value.length;
            chatInput.selectionEnd = chatInput.value.length;
          }
        }, 300);
      }
    }
  };

  return (
    <div ref={containerRef}>
      {children}
      <SelectionActionButton
        selectedText={selectedText}
        position={selectionPosition}
        isVisible={isVisible}
        onAskAI={handleAskAI}
      />
    </div>
  );
};

export default ContextualAIProvider;