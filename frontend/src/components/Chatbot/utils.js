/**
 * Error handling utilities for graceful error handling
 */

/**
 * Format error message for display to user
 * @param {Error|string} error - The error to format
 * @returns {string} User-friendly error message
 */
export const formatErrorMessage = (error) => {
  if (error instanceof Error) {
    // Handle network errors
    if (error.message.includes('Network error')) {
      return 'Unable to connect to the documentation service. Please check your connection and try again.';
    }

    // Handle HTTP errors
    if (error.message.includes('HTTP error')) {
      return 'The documentation service is temporarily unavailable. Please try again later.';
    }

    // Handle other errors
    return `An error occurred: ${error.message}`;
  }

  // Handle string errors
  if (typeof error === 'string') {
    return error;
  }

  // Fallback for unknown error types
  return 'An unexpected error occurred. Please try again.';
};

/**
 * Log error with context
 * @param {Error} error - The error to log
 * @param {string} context - Context where the error occurred
 */
export const logError = (error, context = '') => {
  console.error(`[${context || 'Chatbot'} Error]:`, error);

  // In a real application, you might send this to an error tracking service
  // For example: Sentry.captureException(error);
};

/**
 * Check if an error is a network error
 * @param {Error} error - The error to check
 * @returns {boolean} Whether the error is a network error
 */
export const isNetworkError = (error) => {
  return error.message.includes('Network error') ||
         error.message.includes('fetch') ||
         error.message.includes('Failed to fetch');
};

/**
 * Generate a unique ID for messages
 * @returns {string} Unique identifier
 */
export const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

/**
 * Format timestamp for display
 * @param {Date|number} timestamp - The timestamp to format
 * @returns {string} Formatted timestamp
 */
export const formatTimestamp = (timestamp = Date.now()) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

export default {
  formatErrorMessage,
  logError,
  isNetworkError,
  generateId,
  formatTimestamp,
};