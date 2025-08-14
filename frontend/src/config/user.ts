// Centralized user configuration for frontend
// This ensures consistent user identification across all components

export const DEFAULT_USER_CONFIG = {
  // Default user for testing and development
  DEFAULT_COGNITO_SUB: 'frontend-test-user',
  
  // Fallback UUID for components that need UUID format
  DEFAULT_USER_UUID: 'dc5fd330-8226-4eee-9333-1a61ab3c0381',
  
  // Test user profile
  DEFAULT_USER_PROFILE: {
    email: 'frontend@test.com',
    full_name: 'Frontend Test User',
    cognito_sub: 'frontend-test-user'
  }
};

// Helper function to get the current user ID
export const getCurrentUserId = (): string => {
  // In a real app, this would come from authentication context
  // For now, return the test user
  return DEFAULT_USER_CONFIG.DEFAULT_COGNITO_SUB;
};

// Helper function to get current user UUID (for endpoints that require UUID format)
export const getCurrentUserUUID = (): string => {
  return DEFAULT_USER_CONFIG.DEFAULT_USER_UUID;
};

export default DEFAULT_USER_CONFIG;
