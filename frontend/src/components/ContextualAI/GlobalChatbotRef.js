// Global reference to the chatbot widget for cross-component communication
let globalChatbotRef = null;

export const setGlobalChatbotRef = (ref) => {
  globalChatbotRef = ref;
};

export const getGlobalChatbotRef = () => {
  return globalChatbotRef;
};