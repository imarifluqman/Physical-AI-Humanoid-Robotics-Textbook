import { useState, useEffect, useRef } from 'react';

/**
 * Custom hook for handling text selection detection
 * Monitors text selection and provides selected text and position
 */
export const useTextSelection = () => {
  const [selectedText, setSelectedText] = useState('');
  const [selectionPosition, setSelectionPosition] = useState({ x: 0, y: 0 });
  const [isVisible, setIsVisible] = useState(false);

  // Refs for debouncing rapid selection changes
  const timeoutRef = useRef(null);

  // Function to get selection coordinates
  const getSelectionPosition = () => {
    const selection = window.getSelection();
    if (!selection || selection.toString().trim() === '' || selection.rangeCount === 0) {
      return null;
    }

    try {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      // Position the button near the selection but not blocking it
      // The rect coordinates are relative to the viewport, so add scroll position to get absolute position
      return {
        x: rect.left + window.scrollX,
        y: rect.top + window.scrollY
      };
    } catch (error) {
      // If we can't get the range (e.g., selection is collapsed), return null
      return null;
    }
  };

  // Function to handle text selection
  const handleSelection = () => {
    // Clear any existing timeout to debounce rapid selection changes
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set a new timeout to handle the selection after a short delay
    timeoutRef.current = setTimeout(() => {
      const selection = window.getSelection();
      if (!selection) {
        setIsVisible(false);
        setSelectedText('');
        return;
      }

      let text = selection.toString().trim();

      // Check if there's actually a selection range
      if (selection.rangeCount === 0 || !text) {
        setIsVisible(false);
        setSelectedText('');
        return;
      }

      // Implement selection validation to ignore empty/whitespace selections
      if (text) {
        // Handle very long text selections (e.g., entire page content)
        if (text.length > 1000) {
          // Truncate to a reasonable length while preserving sentence boundaries
          text = text.substring(0, 1000);
          // Try to find the last sentence end before truncation
          const lastSentence = text.lastIndexOf('.');
          if (lastSentence > 500) { // Only if the sentence is reasonably long
            text = text.substring(0, lastSentence + 1);
          }
          text += '...'; // Indicate that the text was truncated
        }

        const position = getSelectionPosition();
        if (position) {
          setSelectedText(text);
          setSelectionPosition(position);
          setIsVisible(true);
        } else {
          // If we can't get position, don't show the button
          setIsVisible(false);
          setSelectedText('');
        }
      } else {
        setIsVisible(false);
        setSelectedText('');
      }
    }, 100); // 100ms delay to debounce rapid changes
  };

  // Function to hide the button
  const hideButton = () => {
    setIsVisible(false);
    setSelectedText('');
  };

  // Add event listeners for 'mouseup', 'selectionchange', and other events
  useEffect(() => {
    const handleMouseUp = () => {
      setTimeout(() => { // Use setTimeout to ensure selection is complete
        handleSelection();
      }, 0);
    };

    const handleSelectionChange = () => {
      handleSelection();
    };

    const handleKeyDown = (e) => {
      // Hide button if user presses Escape
      if (e.key === 'Escape') {
        hideButton();
      }
    };

    // Handle scroll events to update button position
    const handleScroll = () => {
      if (isVisible && selectedText) {
        // Update the position to follow the selected text as the page scrolls
        const newPosition = getSelectionPosition();
        if (newPosition) {
          setSelectionPosition(newPosition);
        }
      }
    };

    // Handle page navigation events to hide button appropriately
    const handleNavigation = () => {
      setIsVisible(false);
      setSelectedText('');
    };

    // Add event listeners
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('keyup', handleKeyDown);
    window.addEventListener('scroll', handleScroll, true); // Use capture phase to catch all scroll events

    // Listen for navigation events (popstate for browser back/forward, hashchange for anchor links)
    window.addEventListener('popstate', handleNavigation);
    window.addEventListener('hashchange', handleNavigation);

    // Cleanup to prevent memory leaks
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('keyup', handleKeyDown);
      window.removeEventListener('scroll', handleScroll, true);
      window.removeEventListener('popstate', handleNavigation);
      window.removeEventListener('hashchange', handleNavigation);

      // Clear any pending timeouts
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []); // Empty dependency array to ensure event listeners are only set up once

  return {
    selectedText,
    selectionPosition,
    isVisible,
    hideButton
  };
};