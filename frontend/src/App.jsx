// frontend/src/App.jsx - FINAL CLEAN VERSION - NO DUPLICATES
import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';

// Import only essential Berry components
import { ConfigProvider } from './contexts/ConfigContext';
import ThemeCustomization from './themes';

// Import your dashboard component
import Dashboard from './components/dashboard/Dashboard';

// Clean single-page layout - NO DUPLICATES
const KairoCalLayout = ({ children }) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const handleLogout = () => {
    // Clear any stored auth data
    localStorage.removeItem('isAuthenticated');
    sessionStorage.clear();
    
    // Redirect to landing/login page
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
            <div style={{
              backgroundColor: '#3b82f6',
              padding: '8px',
              borderRadius: '10px',
              fontSize: '20px'
            }}>
              📅
            </div>
            {!sidebarCollapsed && (
              <div>
                <div style={{ 
                  fontSize: '20px', 
                  fontWeight: '700',
                  color: '#f8fafc'
                }}>
                  KairoCal
                </div>
                <div style={{
                  fontSize: '12px',
                  color: '#94a3b8'
                }}>
                  Smart Calendar
                </div>
              </div>
            )}
          </div>
          
          {/* Hamburger Toggle Button */}
          <button
            onClick={toggleSidebar}
            style={{
              background: 'none',
              border: 'none',
              color: '#94a3b8',
              cursor: 'pointer',
              padding: '8px',
              borderRadius: '6px',
              display: 'flex',
              flexDirection: 'column',
              gap: '3px',
              alignItems: 'center',
              justifyContent: 'center',
              width: '24px',
              height: '24px'
            }}
          >
            <div style={{ width: '16px', height: '2px', backgroundColor: '#94a3b8', borderRadius: '1px' }}></div>
            <div style={{ width: '16px', height: '2px', backgroundColor: '#94a3b8', borderRadius: '1px' }}></div>
            <div style={{ width: '16px', height: '2px', backgroundColor: '#94a3b8', borderRadius: '1px' }}></div>
          </button>
        </div>
        
        {/* Navigation */}
        <nav style={{ 
          flex: 1, 
          padding: '24px 16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '4px'
        }}>
          <NavItem 
            href="/dashboard" 
            icon="🏠" 
            label="Dashboard" 
            active={window.location.pathname.includes('dashboard')}
            collapsed={sidebarCollapsed}
          />
          <NavItem 
            href="/settings" 
            icon="⚙️" 
            label="Settings"
            active={window.location.pathname.includes('settings')}
            collapsed={sidebarCollapsed}
          />
          <NavItem 
            href="/calendar" 
            icon="📅" 
            label="Calendar"
            active={window.location.pathname.includes('calendar')}
            collapsed={sidebarCollapsed}
          />
          <NavItem 
            href="/notifications" 
            icon="🔔" 
            label="Notifications"
            active={window.location.pathname.includes('notifications')}
            collapsed={sidebarCollapsed}
          />
          <NavItem 
            href="/help" 
            icon="❓" 
            label="Help & Support"
            active={window.location.pathname.includes('help')}
            collapsed={sidebarCollapsed}
          />
        </nav>
      </div>

      {/* Main Content Area */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#f8fafc',
        overflow: 'hidden',
        minWidth: 0,
        width: '100%'
      }}>
        {/* Header */}
        <header style={{
          backgroundColor: 'white',
          padding: '16px 32px',
          borderBottom: '1px solid #e2e8f0',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          minHeight: '72px',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
          width: '100%',
          minWidth: 0,
          flexShrink: 0
        }}>
          <div style={{ flex: 1 }}>
            {/* Empty space - no dashboard heading */}
          </div>
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '16px'
          }}>
            {/* Search */}
            <div style={{
              position: 'relative',
              display: 'flex',
              alignItems: 'center'
            }}>
              <input
                type="text"
                placeholder="Search..."
                style={{
                  padding: '8px 12px 8px 36px',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  fontSize: '14px',
                  width: '200px',
                  outline: 'none'
                }}
              />
              <span style={{
                position: 'absolute',
                left: '12px',
                color: '#94a3b8'
              }}>
                🔍
              </span>
            </div>

            {/* Notifications */}
            <button style={{
              background: 'none',
              border: 'none',
              fontSize: '20px',
              cursor: 'pointer',
              padding: '8px',
              borderRadius: '8px',
              position: 'relative'
            }}>
              🔔
              <span style={{
                position: 'absolute',
                top: '6px',
                right: '6px',
                width: '8px',
                height: '8px',
                backgroundColor: '#ef4444',
                borderRadius: '50%'
              }}></span>
            </button>

            {/* User Profile Dropdown */}
            <div style={{ position: 'relative' }}>
              <div 
                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 12px',
                  backgroundColor: '#f8fafc',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  border: '1px solid #e2e8f0'
                }}
              >
                <div style={{
                  width: '32px',
                  height: '32px',
                  backgroundColor: '#3b82f6',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '14px',
                  fontWeight: '600'
                }}>
                  U
                </div>
                <div style={{ textAlign: 'left' }}>
                  <div style={{
                    fontSize: '14px',
                    fontWeight: '500',
                    color: '#1e293b'
                  }}>
                    User Name
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: '#64748b'
                  }}>
                    user@example.com
                  </div>
                </div>
                <span style={{ 
                  fontSize: '12px', 
                  color: '#94a3b8',
                  transform: userDropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.2s'
                }}>
                  ▼
                </span>
              </div>

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
                    🚪 Logout
                  </button>
                </div>
              )}
            </div>
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
          {/* REMOVED DUPLICATE SEARCH BAR */}

          {/* REMOVED CONFLICT ALERT - NO LONGER NEEDED */}

          {/* SINGLE Dashboard Container - NO DUPLICATES */}
          <div style={{
            backgroundColor: 'white',
            borderRadius: '16px',
            padding: '0',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
            minHeight: '600px',
            overflow: 'auto'
          }}>
            {/* YOUR ORIGINAL DASHBOARD COMPONENT - UNCHANGED */}
            <Dashboard />
          </div>
        </main>
      </div>
    </div>
  );
};

// Navigation Item Component
const NavItem = ({ href, icon, label, active, collapsed }) => (
  <a 
    href={href} 
    style={{ 
      color: active ? '#3b82f6' : '#94a3b8',
      backgroundColor: active ? '#1e40af20' : 'transparent',
      textDecoration: 'none',
      display: 'flex',
      alignItems: 'center',
      gap: collapsed ? '0' : '12px',
      padding: collapsed ? '12px' : '12px 16px',
      borderRadius: '12px',
      fontSize: '14px',
      fontWeight: '500',
      transition: 'all 0.2s ease',
      border: active ? '1px solid #3b82f620' : '1px solid transparent',
      justifyContent: collapsed ? 'center' : 'flex-start'
    }}
    title={collapsed ? label : ''}
    onMouseEnter={(e) => {
      if (!active) {
        e.target.style.backgroundColor = '#1e293b';
        e.target.style.color = '#f8fafc';
      }
    }}
    onMouseLeave={(e) => {
      if (!active) {
        e.target.style.backgroundColor = 'transparent';
        e.target.style.color = '#94a3b8';
      }
    }}
  >
    <span style={{ fontSize: '16px' }}>{icon}</span>
    {!collapsed && label}
  </a>
);

// Simple Login/Landing Page
const LoginPage = () => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
    fontFamily: '"Inter", "Roboto", sans-serif'
  }}>
    <div style={{
      backgroundColor: 'white',
      padding: '48px',
      borderRadius: '16px',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
      textAlign: 'center',
      maxWidth: '400px',
      width: '100%'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '12px',
        marginBottom: '32px'
      }}>
        <div style={{
          backgroundColor: '#3b82f6',
          padding: '12px',
          borderRadius: '12px',
          fontSize: '24px'
        }}>
          📅
        </div>
        <div>
          <h1 style={{
            margin: 0,
            fontSize: '28px',
            fontWeight: '700',
            color: '#1e293b'
          }}>
            KairoCal
          </h1>
          <p style={{
            margin: '4px 0 0 0',
            fontSize: '14px',
            color: '#64748b'
          }}>
            Smart Calendar
          </p>
        </div>
      </div>
      
      <h2 style={{
        fontSize: '24px',
        fontWeight: '600',
        color: '#1e293b',
        margin: '0 0 8px 0'
      }}>
        Welcome Back
      </h2>
      
      <p style={{
        fontSize: '16px',
        color: '#64748b',
        margin: '0 0 32px 0'
      }}>
        Sign in to access your smart calendar
      </p>
      
      <button
        onClick={() => window.location.href = '/dashboard'}
        style={{
          width: '100%',
          padding: '12px 24px',
          backgroundColor: '#3b82f6',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          fontSize: '16px',
          fontWeight: '500',
          cursor: 'pointer',
          marginBottom: '16px'
        }}
      >
        Continue to Dashboard
      </button>
      
      <p style={{
        fontSize: '14px',
        color: '#64748b',
        margin: 0
      }}>
        Authentication integration coming soon...
      </p>
    </div>
  </div>
);
const Settings = () => (
  <div style={{ padding: '32px', textAlign: 'center' }}>
    <h2 style={{ color: '#1e293b', marginBottom: '16px' }}>Settings</h2>
    <p style={{ color: '#64748b' }}>Settings page coming soon...</p>
  </div>
);

const Calendar = () => (
  <div style={{ padding: '32px', textAlign: 'center' }}>
    <h2 style={{ color: '#1e293b', marginBottom: '16px' }}>Calendar View</h2>
    <p style={{ color: '#64748b' }}>Full calendar view coming soon...</p>
  </div>
);

const Notifications = () => (
  <div style={{ padding: '32px', textAlign: 'center' }}>
    <h2 style={{ color: '#1e293b', marginBottom: '16px' }}>Notifications</h2>
    <p style={{ color: '#64748b' }}>Notifications page coming soon...</p>
  </div>
);

const Help = () => (
  <div style={{ padding: '32px', textAlign: 'center' }}>
    <h2 style={{ color: '#1e293b', marginBottom: '16px' }}>Help & Support</h2>
    <p style={{ color: '#64748b' }}>Help page coming soon...</p>
  </div>
);

// Global styles
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
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<KairoCalLayout><Dashboard /></KairoCalLayout>} />
            <Route path="/dashboard" element={<KairoCalLayout><Dashboard /></KairoCalLayout>} />
            <Route path="/settings" element={<KairoCalLayout><Settings /></KairoCalLayout>} />
            <Route path="/calendar" element={<KairoCalLayout><Calendar /></KairoCalLayout>} />
            <Route path="/notifications" element={<KairoCalLayout><Notifications /></KairoCalLayout>} />
            <Route path="/help" element={<KairoCalLayout><Help /></KairoCalLayout>} />
          </Routes>
        </ThemeCustomization>
      </ConfigProvider>
    </>
  );
}

export default App;