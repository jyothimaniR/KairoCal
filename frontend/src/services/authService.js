import { Amplify } from 'aws-amplify';
import { signInWithRedirect, fetchAuthSession } from 'aws-amplify/auth';
import awsconfig from '../config/aws-exports';

Amplify.configure(awsconfig);

// Always explicitly login via Cognito Hosted UI
export const login = () => {
  const loginUrl = `https://${awsconfig.oauth.domain}/login?response_type=code&client_id=${awsconfig.aws_user_pools_web_client_id}&redirect_uri=${encodeURIComponent(awsconfig.oauth.redirectSignIn)}`;
  window.location.assign(loginUrl);
};

// Explicit logout that clears both local session AND Cognito SSO cookie
export const logout = () => {
  sessionStorage.clear();
  localStorage.clear();
  
  // Explicitly redirect to Cognito Hosted UI Logout endpoint
  const logoutUrl = `https://${awsconfig.oauth.domain}/logout?client_id=${awsconfig.aws_user_pools_web_client_id}&logout_uri=${encodeURIComponent(awsconfig.oauth.redirectSignOut)}`;
  window.location.assign(logoutUrl);
};

// Handle redirect after login explicitly
export const handleAuthRedirect = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('code')) {
    try {
      const { tokens } = await fetchAuthSession();
      if (tokens) {
        sessionStorage.setItem('accessToken', tokens.accessToken.toString());
        sessionStorage.setItem('idToken', tokens.idToken.toString());
        window.history.replaceState({}, document.title, '/dashboard');
        window.location.replace('/dashboard');
        return tokens;
      }
    } catch (error) {
      console.error('Token exchange error:', error);
      window.location.replace('/');
    }
  }
};

// Simple auth check for ProtectedRoute
export const isAuthenticated = () => {
  return !!sessionStorage.getItem('accessToken');
};
