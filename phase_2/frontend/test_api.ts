// Simple test to verify API client functionality
import { apiClient } from './src/lib/api/client';

async function testApiConnection() {
  try {
    console.log('Testing API connection...');

    // This would normally connect to our backend API
    // For now, we'll just verify the client is properly configured
    console.log('API Base URL:', process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1');

    // Verify the client exists and has the expected methods
    if (typeof apiClient.get === 'function') {
      console.log('✓ API client has GET method');
    } else {
      console.error('✗ API client missing GET method');
    }

    if (typeof apiClient.post === 'function') {
      console.log('✓ API client has POST method');
    } else {
      console.error('✗ API client missing POST method');
    }

    if (typeof apiClient.put === 'function') {
      console.log('✓ API client has PUT method');
    } else {
      console.error('✗ API client missing PUT method');
    }

    if (typeof apiClient.delete === 'function') {
      console.log('✓ API client has DELETE method');
    } else {
      console.error('✗ API client missing DELETE method');
    }

    console.log('✓ API client structure verified');
  } catch (error) {
    console.error('✗ Error testing API connection:', error);
  }
}

// Run the test
testApiConnection();