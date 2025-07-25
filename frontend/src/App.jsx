import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';

// Import only essential Berry components
import { ConfigProvider } from './contexts/ConfigContext';
import ThemeCustomization from './themes';

// Import your dashboard and authentication components
import Dashboard from './components/dashboard/Dashboard';
import AuthPage from './pages/AuthPage';
import ProtectedRoute from './components/auth/ProtectedRoute';

// Clean KairoCalLayout component with improved logout
const KairoCalLayout = ({ children }) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const handleLogout = () => {
    // Clear ALL auth data automatically
    localStorage.clear();
    sessionStorage.clear();
    
    // Clear any browser cache
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => {
          caches.delete(name);
        });
      });
    }
    
    console.log('🧹 All session data cleared automatically');
    
    // Redirect to login page (no more landing page)
    window.location.href = '/login';
  };

  return (
    <div style={{ 
      display: 'flex', 
      height: '100vh',
      width: '100%',
      maxWidth: '100vw',
      margin: 0,
      padding: 0,
      fontFamily: '"Inter", "Roboto", sans-serif',
      overflow: 'hidden',
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0
    }}>
      {/* Sidebar */}
      <div style={{
        width: sidebarCollapsed ? '80px' : '280px',
        minWidth: sidebarCollapsed ? '80px' : '280px',
        backgroundColor: '#0f172a',
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '4px 0 12px rgba(0, 0, 0, 0.15)',
        transition: 'width 0.3s ease',
        flexShrink: 0
      }}>
        {/* Logo Section with Hamburger Toggle */}
        <div style={{ 
          padding: sidebarCollapsed ? '24px 12px' : '24px 20px',
          borderBottom: '1px solid #334155',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ 
            display: 'flex',
            alignItems: 'center',
            gap: sidebarCollapsed ? '0' : '12px'
          }}>
            <span style={{ fontSize: sidebarCollapsed ? '24px' : '28px' }}>📅</span>
            {!sidebarCollapsed && (
              <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold' }}>KairoCal</h2>
            )}
          </div>
          <button
            onClick={toggleSidebar}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              fontSize: '18px',
              padding: '4px'
            }}
          >
            ☰
          </button>
        </div>

        {/* Navigation Items */}
        <nav style={{ flex: 1, padding: '20px 0' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <a href="/dashboard" style={{ 
              color: '#3b82f6',
              backgroundColor: '#1e40af20',
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: sidebarCollapsed ? '0' : '12px',
              padding: sidebarCollapsed ? '12px' : '12px 20px',
              margin: '0 12px',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '500',
              justifyContent: sidebarCollapsed ? 'center' : 'flex-start'
            }}>
              <span>🏠</span>
              {!sidebarCollapsed && <span>Dashboard</span>}
            </a>
            
            <a href="/calendar" style={{ 
              color: '#94a3b8',
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: sidebarCollapsed ? '0' : '12px',
              padding: sidebarCollapsed ? '12px' : '12px 20px',
              margin: '0 12px',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '500',
              justifyContent: sidebarCollapsed ? 'center' : 'flex-start'
            }}>
              <span>📅</span>
              {!sidebarCollapsed && <span>Calendar</span>}
            </a>
            
            <a href="/settings" style={{ 
              color: '#94a3b8',
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: sidebarCollapsed ? '0' : '12px',
              padding: sidebarCollapsed ? '12px' : '12px 20px',
              margin: '0 12px',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '500',
              justifyContent: sidebarCollapsed ? 'center' : 'flex-start'
            }}>
              <span>⚙️</span>
              {!sidebarCollapsed && <span>Settings</span>}
            </a>
            
            <a href="/notifications" style={{ 
              color: '#94a3b8',
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: sidebarCollapsed ? '0' : '12px',
              padding: sidebarCollapsed ? '12px' : '12px 20px',
              margin: '0 12px',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '500',
              justifyContent: sidebarCollapsed ? 'center' : 'flex-start'
            }}>
              <span>🔔</span>
              {!sidebarCollapsed && <span>Notifications</span>}
            </a>
            
            <a href="/help" style={{ 
              color: '#94a3b8',
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: sidebarCollapsed ? '0' : '12px',
              padding: sidebarCollapsed ? '12px' : '12px 20px',
              margin: '0 12px',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '500',
              justifyContent: sidebarCollapsed ? 'center' : 'flex-start'
            }}>
              <span>❓</span>
              {!sidebarCollapsed && <span>Help</span>}
            </a>
          </div>
        </nav>
      </div>

      {/* Main Content Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <header style={{
          height: '72px',
          backgroundColor: 'white',
          borderBottom: '1px solid #e2e8f0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 32px',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
          zIndex: 10
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <h1 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#1e293b',
              margin: 0
            }}>
              📅 KairoCal
            </h1>
          </div>

          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setUserDropdownOpen(!userDropdownOpen)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '8px 12px',
                borderRadius: '8px',
                transition: 'background-color 0.2s'
              }}
            >
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                backgroundColor: '#3b82f6',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                fontWeight: 'bold'
              }}>
                U
              </div>
              <div style={{ textAlign: 'left' }}>
                <div style={{ fontSize: '14px', fontWeight: '600', color: '#1e293b' }}>User Name</div>
                <div style={{ fontSize: '12px', color: '#64748b' }}>user@example.com</div>
              </div>
              <span style={{
                fontSize: '12px',
                color: '#64748b',
                transform: userDropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.2s'
              }}>
                ▼
              </span>
            </button>

            {/* Dropdown Menu */}
            {userDropdownOpen && (
              <div style={{
                position: 'absolute',
                top: '100%',
                right: '0',
                marginTop: '8px',
                backgroundColor: 'white',
                borderRadius: '12px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                border: '1px solid #e2e8f0',
                minWidth: '180px',
                zIndex: 1000
              }}>
                <a href="/profile" style={{
                  display: 'block',
                  padding: '12px 16px',
                  color: '#1e293b',
                  textDecoration: 'none',
                  fontSize: '14px',
                  borderBottom: '1px solid #f1f5f9'
                }}>
                  👤 Profile
                </a>
                <button 
                  onClick={handleLogout}
                  style={{
                    display: 'block',
                    width: '100%',
                    padding: '12px 16px',
                    color: '#dc2626',
                    textDecoration: 'none',
                    fontSize: '14px',
                    background: 'none',
                    border: 'none',
                    textAlign: 'left',
                    cursor: 'pointer'
                  }}
                >
                  🚪 Logout (Auto-Clear)
                </button>
              </div>
            )}
          </div>
        </header>

        {/* Main Content */}
        <main style={{
          flex: 1,
          padding: '24px 32px',
          overflow: 'auto',
          backgroundColor: '#f8fafc',
          width: '100%',
          minWidth: 0,
          maxHeight: 'calc(100vh - 72px)'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '16px',
            padding: '0',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
            minHeight: '600px',
            overflow: 'auto'
          }}>
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

// Global styles component
const GlobalStyles = () => (
  <style>
    {`
      * {
        box-sizing: border-box;
      }
      
      body, html, #root {
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
        overflow: hidden;
        position: relative;
      }
      
      body {
        font-family: "Inter", "Roboto", sans-serif;
      }

      ::-webkit-scrollbar {
        width: 8px;
      }

      ::-webkit-scrollbar-track {
        background: #f1f1f1;
      }

      ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
      }

      ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
      }
    `}
  </style>
);

function App() {
  return (
    <>
      <GlobalStyles />
      <ConfigProvider>
        <ThemeCustomization>
          <Routes>
            {/* Root redirects to login - NO MORE LANDING PAGE */}
            <Route path="/" element={<AuthPage />} />
            
            {/* Login page - SINGLE ENTRY POINT */}
            <Route path="/login" element={<AuthPage />} />
            
            {/* Protected dashboard routes */}
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <KairoCalLayout><Dashboard /></KairoCalLayout>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/settings" 
              element={
                <ProtectedRoute>
                  <KairoCalLayout>
                    <div style={{padding: '40px', textAlign: 'center'}}>
                      <h2>Settings coming soon...</h2>
                    </div>
                  </KairoCalLayout>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/calendar" 
              element={
                <ProtectedRoute>
                  <KairoCalLayout><Dashboard /></KairoCalLayout>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/notifications" 
              element={
                <ProtectedRoute>
                  <KairoCalLayout>
                    <div style={{padding: '40px', textAlign: 'center'}}>
                      <h2>Notifications coming soon...</h2>
                    </div>
                  </KairoCalLayout>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/help" 
              element={
                <ProtectedRoute>
                  <KairoCalLayout>
                    <div style={{padding: '40px', textAlign: 'center'}}>
                      <h2>Help coming soon...</h2>
                    </div>
                  </KairoCalLayout>
                </ProtectedRoute>
              } 
            />
          </Routes>
        </ThemeCustomization>
      </ConfigProvider>
    </>
  );
}

export default App;