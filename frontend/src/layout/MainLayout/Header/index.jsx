import React, { useState, useEffect } from 'react';
import { logout } from '../../../services/authService';
import { userMenuItems } from '../../../config/userMenu';

const Topbar = ({ onToggleSidebar }) => {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [userInfo, setUserInfo] = useState({
    name: 'John Doe',
    email: 'john.doe@example.com',
    avatar: null
  });

  // Get user info from Cognito/session
  useEffect(() => {
    // In a real app, you'd get this from Cognito user attributes
    const email = sessionStorage.getItem('userEmail') || 'john.doe@example.com';
    const name = email.split('@')[0].replace('.', ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    setUserInfo({
      name,
      email,
      avatar: null
    });
  }, []);

  const handleUserMenuClick = (action) => {
    switch (action) {
      case 'goToProfile':
        // Navigate to profile page
        console.log('Navigate to profile');
        break;
      case 'logout':
        logout();
        break;
      default:
        console.log('Unknown action:', action);
    }
    setShowUserMenu(false);
  };

  const handleClickOutside = (e) => {
    if (!e.target.closest('.user-menu-container')) {
      setShowUserMenu(false);
    }
  };

  useEffect(() => {
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .substring(0, 2);
  };

  return (
    <header style={{
      height: '64px',
      backgroundColor: 'white',
      borderBottom: '1px solid #e5e7eb',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 999
    }}>
      {/* Left Side - Hamburger Menu */}
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <button
          onClick={onToggleSidebar}
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '8px',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'background-color 0.2s'
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#f3f4f6'}
          onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
        >
          <div style={{
            width: '20px',
            height: '14px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
            <div style={{
              height: '2px',
              backgroundColor: '#6b7280',
              borderRadius: '1px'
            }} />
            <div style={{
              height: '2px',
              backgroundColor: '#6b7280',
              borderRadius: '1px'
            }} />
            <div style={{
              height: '2px',
              backgroundColor: '#6b7280',
              borderRadius: '1px'
            }} />
          </div>
        </button>
      </div>

      {/* Right Side - Notifications and User Info */}
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '16px' 
      }}>
        {/* Notifications Bell */}
        <button style={{
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          padding: '8px',
          borderRadius: '6px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          transition: 'background-color 0.2s'
        }}
        onMouseEnter={(e) => e.target.style.backgroundColor = '#f3f4f6'}
        onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
        >
          <span style={{ 
            fontSize: '18px',
            color: '#6b7280'
          }}>
            🔔
          </span>
          {/* Notification dot */}
          <div style={{
            position: 'absolute',
            top: '6px',
            right: '6px',
            width: '8px',
            height: '8px',
            backgroundColor: '#ef4444',
            borderRadius: '50%',
            border: '2px solid white'
          }} />
        </button>

        {/* User Info and Dropdown */}
        <div className="user-menu-container" style={{ position: 'relative' }}>
          <div
            onClick={() => setShowUserMenu(!showUserMenu)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              cursor: 'pointer',
              padding: '6px 12px',
              borderRadius: '8px',
              transition: 'background-color 0.2s'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = '#f9fafb'}
            onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
          >
            {/* User Avatar */}
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              backgroundColor: '#4f46e5',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '14px',
              fontWeight: '600'
            }}>
              {userInfo.avatar ? (
                <img 
                  src={userInfo.avatar} 
                  alt={userInfo.name}
                  style={{ 
                    width: '100%', 
                    height: '100%', 
                    borderRadius: '50%',
                    objectFit: 'cover'
                  }}
                />
              ) : (
                getInitials(userInfo.name)
              )}
            </div>

            {/* User Info */}
            <div style={{ textAlign: 'left' }}>
              <div style={{
                fontSize: '14px',
                fontWeight: '600',
                color: '#1f2937',
                lineHeight: '1.2'
              }}>
                Hi, {userInfo.name.split(' ')[0]}
              </div>
              <div style={{
                fontSize: '12px',
                color: '#6b7280',
                lineHeight: '1.2'
              }}>
                {userInfo.email}
              </div>
            </div>

            {/* Dropdown Arrow */}
            <div style={{
              fontSize: '12px',
              color: '#9ca3af',
              transform: showUserMenu ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.2s'
            }}>
              ▼
            </div>
          </div>

          {/* User Dropdown Menu */}
          {showUserMenu && (
            <div style={{
              position: 'absolute',
              top: '100%',
              right: 0,
              marginTop: '8px',
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
              minWidth: '180px',
              zIndex: 1000
            }}>
              {userMenuItems.map((item, index) => (
                <button
                  key={index}
                  onClick={() => handleUserMenuClick(item.action)}
                  style={{
                    width: '100%',
                    textAlign: 'left',
                    padding: '12px 16px',
                    border: 'none',
                    background: 'none',
                    fontSize: '14px',
                    color: '#374151',
                    cursor: 'pointer',
                    borderRadius: index === 0 ? '8px 8px 0 0' : 
                               index === userMenuItems.length - 1 ? '0 0 8px 8px' : '0',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#f9fafb'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                >
                  {item.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Topbar;