// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

// Application Constants
export const APP_NAME = 'Todo App';
export const DEFAULT_PAGE_SIZE = 10;
export const REFRESH_INTERVAL = 30000; // 30 seconds

// Local Storage Keys
export const ACCESS_TOKEN_KEY = 'access_token';
export const REFRESH_TOKEN_KEY = 'refresh_token';
export const USER_PREFERENCES_KEY = 'user_preferences';

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred',
  UNAUTHORIZED: 'Unauthorized access',
  SERVER_ERROR: 'Server error occurred',
  VALIDATION_ERROR: 'Validation error occurred',
};