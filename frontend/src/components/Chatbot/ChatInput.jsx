import React, { useState, useEffect, useImperativeHandle, forwardRef, memo } from 'react';
import clsx from 'clsx';
import styles from './ChatInput.module.css';

/**
 * Component for message input with submit button and Enter key support
 * @param {Object} props - Component props
 * @param {Function} props.onSubmit - Function to call when message is submitted
 * @param {boolean} [props.disabled] - Whether the input is disabled
 * @param {boolean} [props.loading] - Whether the component is in loading state
 */
const ChatInput = forwardRef(({ onSubmit, disabled = false, loading = false }, ref) => {
  const [inputValue, setInputValue] = useState('');

  // Expose methods to parent components via ref
  useImperativeHandle(ref, () => ({
    setInputValue: (value) => {
      setInputValue(value);
    },
    getInputValue: () => inputValue,
    clearInput: () => {
      setInputValue('');
    },
    focus: () => {
      // Get the textarea element and focus it
      const textarea = document.querySelector(`.${styles.textInput}`);
      if (textarea) {
        textarea.focus();
      }
    }
  }));

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled && !loading) {
      onSubmit(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className={styles.chatInputForm} onSubmit={handleSubmit} role="form">
      <div className={styles.inputContainer}>
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your question here..."
          disabled={disabled || loading}
          className={styles.textInput}
          rows={1}
          aria-label="Chat message input"
          aria-describedby="chat-input-help"
          autoComplete="off"
        />
        <button
          type="submit"
          disabled={disabled || loading || !inputValue.trim()}
          className={clsx(styles.submitButton, loading && styles.loading)}
          aria-label="Send message"
          aria-disabled={disabled || loading || !inputValue.trim()}
        >
          {loading ? (
            <span className={styles.loadingSpinner} aria-label="Sending message">Sending...</span>
          ) : (
            <span className={styles.submitIcon} aria-hidden="true">➤</span>
          )}
        </button>
      </div>
      <div id="chat-input-help" className={styles.inputHelpText} style={{ display: 'none' }}>
        Press Enter to submit, Shift+Enter for new line
      </div>
    </form>
  );
});

export default memo(ChatInput);