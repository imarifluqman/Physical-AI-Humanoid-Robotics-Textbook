import React, { useState, useRef, forwardRef, useImperativeHandle } from 'react';
import Chatbot from './Chatbot';
import styles from './FloatingChatWidget.module.css';

/**
 * Floating chat widget that can be integrated into Docusaurus layout
 */
const FloatingChatWidget = forwardRef((props, ref) => {
  const [isOpen, setIsOpen] = useState(false);
  const chatbotRef = useRef(null);

  // Expose methods to parent components via ref
  useImperativeHandle(ref, () => ({
    openChat: () => setIsOpen(true),
    closeChat: () => setIsOpen(false),
    toggleChat: () => setIsOpen(!isOpen),
    isOpen: () => isOpen,
    setInputValue: (value) => {
      if (chatbotRef.current && chatbotRef.current.setInputValue) {
        chatbotRef.current.setInputValue(value);
      }
    },
    getInputValue: () => {
      if (chatbotRef.current && chatbotRef.current.getInputValue) {
        return chatbotRef.current.getInputValue();
      }
      return '';
    },
    focusInput: () => {
      if (chatbotRef.current && chatbotRef.current.focusInput) {
        chatbotRef.current.focusInput();
      }
    },
    submitMessage: (message) => {
      if (chatbotRef.current && chatbotRef.current.submitMessage) {
        chatbotRef.current.submitMessage(message);
      }
    }
  }));

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.floatingChatContainer} role="complementary" aria-label="Documentation chat assistant">
      {isOpen ? (
        <div
          className={styles.chatWidget}
          role="dialog"
          aria-modal="true"
          aria-label="Chat window"
        >
          <div className={styles.chatHeader}>
            <span>Documentation Assistant</span>
            <button
              className={styles.closeButton}
              onClick={toggleChat}
              aria-label="Close chat"
              title="Close chat"
            >
              ×
            </button>
          </div>
          <div className={styles.chatBody} role="region" aria-label="Chat messages">
            <Chatbot ref={chatbotRef} hideHeader={true} />
          </div>
        </div>
      ) : (
        <button
          className={styles.fab}
          onClick={toggleChat}
          aria-label="Open documentation chat"
          title="Open documentation chat"
        >
          <span className={styles.fabIcon} aria-hidden="true">💬</span>
        </button>
      )}
    </div>
  );
});

export default FloatingChatWidget;