import React, { useState, useCallback, useRef, useEffect, useImperativeHandle, forwardRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import styles from './Chatbot.module.css';
import { formatErrorMessage, logError, generateId } from './utils';
import { sendQuery } from './api';

/**
 * Main Chatbot component implementing chat functionality
 * Enables users to ask questions and receive AI-generated responses
 */
const Chatbot = forwardRef(({ hideHeader = false }, ref) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Refs for accessing DOM elements and current messages
  const messagesEndRef = useRef(null);
  const messagesRef = useRef(messages);
  messagesRef.current = messages;
  const chatInputRef = useRef(null);

  // Expose methods to parent components via ref
  useImperativeHandle(ref, () => ({
    setInputValue: (value) => {
      if (chatInputRef.current && chatInputRef.current.setInputValue) {
        chatInputRef.current.setInputValue(value);
      }
    },
    getInputValue: () => {
      if (chatInputRef.current && chatInputRef.current.getInputValue) {
        return chatInputRef.current.getInputValue();
      }
      return '';
    },
    clearInput: () => {
      if (chatInputRef.current && chatInputRef.current.clearInput) {
        chatInputRef.current.clearInput();
      }
    },
    focusInput: () => {
      if (chatInputRef.current && chatInputRef.current.focus) {
        chatInputRef.current.focus();
      }
    },
    submitMessage: (message) => {
      handleCustomSubmit(message);
    },
    getMessages: () => messages,
    clearMessages: () => {
      setMessages([]);
      setError(null);
      setIsLoading(false);
    }
  }));

  // Handle message submission
  const handleCustomSubmit = useCallback(async (message) => {
    if (!message.trim()) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message to the chat
      const userMessage = {
        id: generateId(),
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, userMessage]);

      // Call our backend API with just the user's query (not the full message history)
      // The backend handles conversation context internally if needed
      const response = await sendQuery(userMessage.content);
      console.log("res", response.answer);

      // Add assistant response to the chat
      // The backend returns a response object with an 'answer' field
      const assistantMessage = {
        id: generateId(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      logError(err, 'Chatbot Submit');
      setError(err);

      // Add error message to chat
      const errorMessage = {
        id: generateId(),
        role: 'assistant',
        content: formatErrorMessage(err),
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []); // Now we can use an empty dependency array since we're using the ref

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className={styles.chatbotContainer} role="main" aria-label="Documentation chat assistant">
      {!hideHeader && (
        <div className={styles.chatHeader}>
          <h3>Documentation Assistant</h3>
        </div>
      )}

      <div
        className={styles.chatMessages}
        aria-live="polite"
        aria-relevant="additions"
        role="log"
      >
        {messages.map((msg) => (
          <ChatMessage
            key={msg.id}
            role={msg.role}
            content={msg.content}
          />
        ))}

        {error && !isLoading && (
          <ChatMessage
            role="assistant"
            content={formatErrorMessage(error)}
          />
        )}

        {isLoading && (
          <ChatMessage
            role="assistant"
            content="Thinking..."
            aria-label="Assistant is thinking"
          />
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.chatInputArea}>
        <ChatInput
          ref={chatInputRef}
          onSubmit={handleCustomSubmit}
          disabled={isLoading}
          loading={isLoading}
        />
      </div>
    </div>
  );
});

export default Chatbot;