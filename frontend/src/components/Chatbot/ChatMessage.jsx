import React, { memo } from 'react';
import clsx from 'clsx';
import styles from './ChatMessage.module.css';

/**
 * Component to render individual chat messages with role-based styling
 * @param {Object} props - Component props
 * @param {string} props.role - Message role ('user' or 'assistant')
 * @param {string} props.content - Message content
 * @param {string} [props.timestamp] - Optional timestamp
 */
const ChatMessage = memo(({ role, content, timestamp }) => {
  const isUser = role === 'user';

  return (
    <div
      className={clsx(styles.message, isUser ? styles.userMessage : styles.assistantMessage)}
      role="listitem"
      aria-label={`${isUser ? 'User' : 'Assistant'} message`}
    >
      <div className={styles.messageContent}>
        <div className={styles.messageText} role="text">{content}</div>
        {timestamp && (
          <div className={styles.timestamp} aria-label={`Message time: ${timestamp}`}>
            {timestamp}
          </div>
        )}
      </div>
    </div>
  );
});

export default ChatMessage;