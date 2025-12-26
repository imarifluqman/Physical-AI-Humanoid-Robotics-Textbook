import React, { createContext, useContext, ReactNode, useState, useCallback, useRef } from 'react';
import { sendQuery } from './api';
import { formatErrorMessage, logError, generateId } from './utils';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ChatbotContextType {
  messages: Message[];
  isLoading: boolean;
  error: any;
  setInputValue: (value: string) => void;
  submitMessage: (message: string) => Promise<void>;
  clearMessages: () => void;
}

const ChatbotContext = createContext<ChatbotContextType | undefined>(undefined);

interface ChatbotProviderProps {
  children: ReactNode;
}

export const ChatbotProvider: React.FC<ChatbotProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const messagesRef = useRef(messages);
  messagesRef.current = messages;

  const submitMessage = useCallback(async (message: string) => {
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

      // Call our backend API with just the user's query
      const response = await sendQuery(userMessage.content);

      // Add assistant response to the chat
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
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
    setIsLoading(false);
  }, []);

  return (
    <ChatbotContext.Provider
      value={{
        messages,
        isLoading,
        error,
        setInputValue,
        submitMessage,
        clearMessages,
      }}
    >
      {children}
    </ChatbotContext.Provider>
  );
};

export const useChatbot = (): ChatbotContextType => {
  const context = useContext(ChatbotContext);
  if (context === undefined) {
    throw new Error('useChatbot must be used within a ChatbotProvider');
  }
  return context;
};