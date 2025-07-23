import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { menuItems } from '../../config/menuItems';

const Sidebar = ({ collapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleMenuClick = (path) => {
    navigate(path);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      height: '100vh',
      width: collapsed ? '60px' : '260px',
      backgroundColor: 'white',
      borderRight: '1px solid #e5e7eb',
      transition: 'width 0.3s ease',
      zIndex: 1000,
      display: 'flex',
      flexDirection: 'column'
    }}>
      {/* Logo Section */}
      <div style={{
        padding: collapsed ? '20px 10px' : '20px',
        borderBottom: '1px solid #f3f4f6',
        textAlign: 'center',
        transition: 'padding 0.3s ease'
      }}>
        {!collapsed ? (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            <div style={{
              width: '36px',
              height: '36px',
              backgroundColor: '#4f46e5',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '18px',
              color: 'white'
            }}>
              📅
            </div>
            <div>
              <h1 style={{
                fontSize: '20px',
                fontWeight: 'bold',
                color: '#1f2937',
                margin: 0
              }}>
                KairoCal
              </h1>
              <p style={{
                fontSize: '12px',
                color: '#6b7280',
                margin: 0
              }}>
                AI Calendar
              </p>
            </div>
          </div>
        ) : (
          <div style={{
            width: '32px',
            height: '32px',
            backgroundColor: '#4f46e5',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '16px',
            color: 'white',
            margin: '0 auto'
          }}>
            📅
          </div>
        )}
      </div>

      {/* Menu Items */}
      <nav style={{ 
        flex: 1, 
        padding: '16px 0',
        overflowY: 'auto'
      }}>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path || 
                          (item.path === '/dashboard' && location.pathname === '/');
          
          return (
            <div
              key={item.path}
              onClick={() => handleMenuClick(item.path)}
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: collapsed ? '12px 16px' : '12px 20px',
                margin: collapsed ? '4px 8px' : '4px 16px',
                borderRadius: '8px',
                cursor: 'pointer',
                backgroundColor: isActive ? '#f0f9ff' : 'transparent',
                color: isActive ? '#0369a1' : '#6b7280',
                transition: 'all 0.2s ease',
                position: 'relative'
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.target.style.backgroundColor = '#f9fafb';
                  e.target.style.color = '#374151';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.target.style.backgroundColor = 'transparent';
                  e.target.style.color = '#6b7280';
                }
              }}
            >
              <Icon 
                style={{ 
                  fontSize: '20px',
                  minWidth: '20px',
                  color: isActive ? '#0369a1' : '#6b7280'
                }} 
              />
              {!collapsed && (
                <span style={{
                  marginLeft: '12px',
                  fontSize: '14px',
                  fontWeight: isActive ? '600' : '500',
                  whiteSpace: 'nowrap'
                }}>
                  {item.title}
                </span>
              )}
              {isActive && (
                <div style={{
                  position: 'absolute',
                  right: 0,
                  top: '50%',
                  transform: 'translateY(-50%)',
                  width: '3px',
                  height: '20px',
                  backgroundColor: '#0369a1',
                  borderRadius: '2px 0 0 2px'
                }} />
              )}
            </div>
          );
        })}
      </nav>

      {/* Footer - User Status */}
      {!collapsed && (
        <div style={{
          padding: '16px 20px',
          borderTop: '1px solid #f3f4f6',
          fontSize: '12px',
          color: '#9ca3af',
          textAlign: 'center'
        }}>
          <div style={{ marginBottom: '4px' }}>
            ✨ AI-Powered
          </div>
          <div>
            Smart Calendar
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;