import React, { useRef, useEffect } from 'react';
import OriginalLayout from '@theme-original/Layout';
import { FloatingChatWidget } from '@site/src/components/Chatbot';
import { ThemeProvider } from '@site/src/components/ThemeContext';
import ContextualAIProvider from '@site/src/components/ContextualAI/ContextualAIProvider';
import { setGlobalChatbotRef } from '@site/src/components/ContextualAI/GlobalChatbotRef';

export default function Layout(props) {
  const chatWidgetRef = useRef(null);

  // Register the chatbot reference globally when component mounts
  useEffect(() => {
    if (chatWidgetRef.current) {
      setGlobalChatbotRef(chatWidgetRef.current);
    }

    // Cleanup on unmount
    return () => {
      setGlobalChatbotRef(null);
    };
  }, []);

  return (
    <ThemeProvider>
      <ContextualAIProvider>
        <>
          <OriginalLayout {...props} />
          <FloatingChatWidget ref={chatWidgetRef} />
        </>
      </ContextualAIProvider>
    </ThemeProvider>
  );
}