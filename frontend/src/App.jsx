import React, { useEffect, useState } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { login, getCurrentAuthUser, logout, isAuthenticated } from "./services/authService";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import Dashboard from "./pages/Dashboard";

const App = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(true);
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    let hubListenerCancelToken;

    const initializeAuth = async () => {
      console.log('🎬 App: Initializing auth on path:', location.pathname);
      setIsLoading(true);

      // Import Hub dynamically to avoid import errors
      try {
        const { Hub } = await import('aws-amplify/utils');
        
        // Set up Hub listener for auth events
        console.log('👂 Setting up Hub listener...');
        hubListenerCancelToken = Hub.listen('auth', ({ payload }) => {
          console.log('🎯 Hub event received:', payload.event);
          
          switch (payload.event) {
            case 'signInWithRedirect':
              console.log('✅ signInWithRedirect completed - user should be authenticated');
              handleSuccessfulAuth();
              break;
            case 'signInWithRedirect_failure':
              console.error('❌ signInWithRedirect failed:', payload.data);
              break;
            case 'signedOut':
              console.log('🚪 User signed out');
              sessionStorage.clear();
              navigate('/', { replace: true });
              break;
          }
        });

        console.log('✅ Hub listener set up successfully');
      } catch (error) {
        console.log('⚠️ Could not set up Hub listener:', error.message);
      }

      // Check current auth status
      await checkAuthStatus();
    };

    const handleSuccessfulAuth = async () => {
      console.log('🔄 Handling successful authentication...');
      try {
        const authUser = await getCurrentAuthUser();
        if (authUser) {
          console.log('✅ Auth user confirmed, navigating to dashboard');
          navigate('/dashboard', { replace: true });
        }
      } catch (error) {
        console.error('❌ Error handling successful auth:', error);
      }
    };

    const checkAuthStatus = async () => {
      try {
        console.log('🔍 Checking current auth status...');
        
        const authUser = await getCurrentAuthUser();
        
        if (authUser) {
          console.log('✅ User is authenticated');
          
          // If user is authenticated but on home page, redirect to dashboard
          if (location.pathname === '/' || location.pathname === '') {
            console.log('🔄 Redirecting authenticated user to dashboard');
            navigate('/dashboard', { replace: true });
          }
        } else {
          console.log('ℹ️ User is not authenticated');
          
          // If user is not authenticated but trying to access protected route
          if (location.pathname === '/dashboard') {
            console.log('🔄 Redirecting unauthenticated user to home');
            navigate('/', { replace: true });
          }
        }
        
      } catch (error) {
        console.error('❌ Auth status check error:', error);
        if (location.pathname === '/dashboard') {
          navigate('/', { replace: true });
        }
      } finally {
        setAuthChecked(true);
        setIsLoading(false);
      }
    };

    initializeAuth();

    // Cleanup
    return () => {
      if (hubListenerCancelToken) {
        console.log('🧹 Cleaning up Hub listener');
        hubListenerCancelToken();
      }
    };
  }, []); // Only run once on mount

  // Show loading while checking auth
  if (isLoading || !authChecked) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">🔄 Checking authentication...</div>
      </div>
    );
  }

  return (
    <Routes>
      <Route
        path="/"
        element={
          <div className="text-center mt-10">
            <h2 className="text-2xl font-bold mb-4">🚀 KairoCal Frontend is Live!</h2>
            <p className="mb-4 text-gray-600">
              {isAuthenticated() ? '✅ You are logged in!' : '🔑 Please log in to continue'}
            </p>
            
            <div className="space-y-4">
              {!isAuthenticated() && (
                <button
                  onClick={login}
                  className="block mx-auto px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  🔐 Login with Cognito
                </button>
              )}
              
              {isAuthenticated() && (
                <div className="space-y-2">
                  <button
                    onClick={() => navigate('/dashboard')}
                    className="block mx-auto px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    📊 Go to Dashboard
                  </button>
                  <button
                    onClick={logout}
                    className="block mx-auto px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                  >
                    🚪 Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default App;