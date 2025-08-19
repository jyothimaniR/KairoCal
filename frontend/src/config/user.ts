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
  },

  // Demo user configuration
  DEMO_USER: {
    cognito_sub: 'demo-user-presentation',
    email: 'demo@kairocal.com',
    full_name: 'Demo User'
  }
};

// Helper function to get the current user ID
export const getCurrentUserId = (): string => {
  // Check for demo mode first
  const demoMode = localStorage.getItem('demoMode') === 'true';
  const demoUserSub = localStorage.getItem('userCognitoSub');
  
  if (demoMode && demoUserSub) {
    return demoUserSub;
  }
  
  // In a real app, this would come from authentication context
  // For now, return the test user
  return DEFAULT_USER_CONFIG.DEFAULT_COGNITO_SUB;
};

// Helper function to get current user UUID (for endpoints that require UUID format)
export const getCurrentUserUUID = (): string => {
  return DEFAULT_USER_CONFIG.DEFAULT_USER_UUID;
};

// Helper function to check if we're in demo mode
export const isDemoMode = (): boolean => {
  return localStorage.getItem('demoMode') === 'true';
};

// Helper function to get demo user info
export const getDemoUserInfo = () => {
  if (isDemoMode()) {
    return {
      email: localStorage.getItem('userEmail') || DEFAULT_USER_CONFIG.DEMO_USER.email,
      sub: localStorage.getItem('userCognitoSub') || DEFAULT_USER_CONFIG.DEMO_USER.cognito_sub,
      full_name: DEFAULT_USER_CONFIG.DEMO_USER.full_name
    };
  }
  return null;
};

export default DEFAULT_USER_CONFIG;
