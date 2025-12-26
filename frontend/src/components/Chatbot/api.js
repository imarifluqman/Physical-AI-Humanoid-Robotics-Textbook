/**
 * API utility functions for backend communication (POST /api/v1/query)
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Function to send a query to the backend API
 * @param {string} query - The user's query string
 * @returns {Promise<Object>} Response from the backend
 */
export const sendQuery = async (query) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.error ||
        `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    return data;
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Unable to connect to the backend service');
    }
    throw error;
  }
};

/**
 * Function to test backend connectivity
 * @returns {Promise<boolean>} Whether the backend is reachable
 */
export const testBackendConnection = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: 'test connection',
      }),
    });

    return response.ok;
  } catch (error) {
    return false;
  }
};

export default {
  sendQuery,
  testBackendConnection,
};