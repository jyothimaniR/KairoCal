import React from 'react';
import { login } from '../services/authService';

const AuthPage = () => {
  const handleLogin = async () => {
    console.log('🚀 AuthPage: Starting login process...');
    await login();
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div style={{
        background: 'white',
        padding: '3rem',
        borderRadius: '12px',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        maxWidth: '400px',
        width: '100%'
      }}>
        {/* Logo/Title */}
        <div style={{ marginBottom: '2rem' }}>
          <h1 style={{
            fontSize: '2.5rem',
            fontWeight: 'bold',
            color: '#4f46e5',
            marginBottom: '0.5rem'
          }}>
            📅 KairoCal
          </h1>
          <p style={{
            color: '#6b7280',
            fontSize: '1.1rem'
          }}>
            AI-Powered Smart Calendar
          </p>
        </div>

        {/* Description */}
        <div style={{ marginBottom: '2rem' }}>
          <p style={{
            color: '#4b5563',
            lineHeight: '1.6'
          }}>
            Welcome to your intelligent calendar assistant. 
            Sign in to start managing your events with natural language.
          </p>
        </div>

        {/* Login Button */}
        <button
          onClick={handleLogin}
          style={{
            width: '100%',
            padding: '12px 24px',
            backgroundColor: '#4f46e5',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s',
            marginBottom: '1rem'
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#4338ca'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#4f46e5'}
        >
          🔐 Sign in with AWS Cognito
        </button>

        {/* Features */}
        <div style={{
          textAlign: 'left',
          padding: '1.5rem',
          backgroundColor: '#f8fafc',
          borderRadius: '8px',
          marginTop: '1.5rem'
        }}>
          <p style={{ 
            fontWeight: '600', 
            marginBottom: '0.5rem',
            color: '#374151'
          }}>
            ✨ Features:
          </p>
          <ul style={{
            margin: 0,
            paddingLeft: '1.2rem',
            color: '#6b7280',
            fontSize: '14px',
            lineHeight: '1.5'
          }}>
            <li>Natural language event creation</li>
            <li>Smart conflict detection</li>
            <li>Intelligent notifications</li>
            <li>Cloud-native architecture</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;