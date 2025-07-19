// authService.js - FINAL FIX using signInWithRedirect
import { Amplify } from 'aws-amplify';
import { signInWithRedirect, getCurrentUser, signOut, fetchAuthSession } from 'aws-amplify/auth';
import awsconfig from '../config/aws-exports';

Amplify.configure(awsconfig);

// Login using signInWithRedirect (CRITICAL FOR AMPLIFY V6)
export const login = async () => {
  console.log('🚀 Starting login with signInWithRedirect...');
  try {
    await signInWithRedirect();
  } catch (error) {
    console.error('❌ Login failed:', error);
  }
};

// Logout
export const logout = async () => {
  console.log('🚪 Logging out...');
  try {
    await signOut();
    sessionStorage.clear();
    localStorage.clear();
  } catch (error) {
    console.error('❌ Logout failed:', error);
  }
};

// Check if user is authenticated
export const isAuthenticated = () => {
  return !!sessionStorage.getItem('isAuthenticated');
};

// Get current user and store auth state
export const getCurrentAuthUser = async () => {
  try {
    console.log('🔍 Checking current user...');
    
    const user = await getCurrentUser();
    console.log('✅ User found:', user.username);
    
    const session = await fetchAuthSession();
    console.log('🎫 Session tokens:', session.tokens ? 'Available' : 'Missing');
    
    if (user && session.tokens) {
      // Store authentication state
      sessionStorage.setItem('isAuthenticated', 'true');
      sessionStorage.setItem('accessToken', session.tokens.accessToken.toString());
      sessionStorage.setItem('idToken', session.tokens.idToken.toString());
      
      console.log('✅ Auth state stored in sessionStorage');
      return { user, session };
    }
    
    return null;
  } catch (error) {
    console.log('ℹ️ User not authenticated:', error.message);
    sessionStorage.clear();
    return null;
  }
};