import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from './contexts/ConfigContext';
import ThemeCustomization from './themes';
import { getCurrentAuthUser } from './services/authService';

// Import components
import AuthPage from './pages/AuthPage';
import MainLayout from './layout/MainLayout';
import ProtectedRoute from './components/auth/ProtectedRoute';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      console.log('🔍 App: Checking authentication status...');
      
      try {
        const authResult = await getCurrentAuthUser();
        if (authResult) {
          console.log('✅ App: User authenticated');
          setIsAuthenticated(true);
        } else {
          console.log('❌ App: User not authenticated');
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.log('❌ App: Auth check failed:', error);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '18px',
        fontFamily: "'Inter', sans-serif"
      }}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '16px'
        }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #f3f4f6',
            borderTop: '4px solid #4f46e5',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }} />
          <div>Loading KairoCal...</div>
        </div>
        <style>
          {`
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `}
        </style>
      </div>
    );
  }

  return (
    <ConfigProvider>
      <ThemeCustomization>
        <Routes>
          {/* Public route for authentication */}
          <Route 
            path="/auth" 
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <AuthPage />
              )
            } 
          />
          
          {/* Protected routes - All dashboard routes */}
          <Route 
            path="/*" 
            element={
              <ProtectedRoute>
                <MainLayout />
              </ProtectedRoute>
            } 
          />
          
          {/* Root redirect */}
          <Route 
            path="/" 
            element={
              <Navigate to={isAuthenticated ? "/dashboard" : "/auth"} replace />
            } 
          />
        </Routes>
      </ThemeCustomization>
    </ConfigProvider>
  );
}

export default App;