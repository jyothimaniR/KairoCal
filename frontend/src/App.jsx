import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { ConfigProvider } from './contexts/ConfigContext';
import ThemeCustomization from './themes';
import { getCurrentAuthUser } from './services/authService';

// Import components
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/auth/ProtectedRoute';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      console.log('🔍 App: Checking authentication status...');
      
      try {
        const authResult = await getCurrentAuthUser();
        if (authResult) {
          console.log('✅ App: User authenticated, redirecting to dashboard');
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
        fontSize: '18px' 
      }}>
        🔄 Loading KairoCal...
      </div>
    );
  }

  return (
    <ConfigProvider>
      <ThemeCustomization>
        <Routes>
          {/* Public route for authentication */}
          <Route 
            path="/" 
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <AuthPage />
              )
            } 
          />
          
          {/* Protected dashboard route */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* Catch all route */}
          <Route 
            path="*" 
            element={<Navigate to={isAuthenticated ? "/dashboard" : "/"} replace />} 
          />
        </Routes>
      </ThemeCustomization>
    </ConfigProvider>
  );
}

export default App;