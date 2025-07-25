import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, getCurrentAuthUser } from '../services/authService';

const AuthPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [checkingAuth, setCheckingAuth] = useState(true);

  // Check if user is already authenticated
  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const authData = await getCurrentAuthUser();
        if (authData) {
          console.log('✅ User already authenticated, redirecting to dashboard');
          navigate('/dashboard', { replace: true });
        }
      } catch (error) {
        console.log('ℹ️ User not authenticated, showing login page');
      } finally {
        setCheckingAuth(false);
      }
    };

    checkAuthentication();
  }, [navigate]);

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    
    try {
      console.log('🚀 Starting Cognito login flow...');
      await login();
      // signInWithRedirect will handle the redirect
    } catch (error) {
      console.error('❌ Login failed:', error);
      setError('Login failed. Please try again.');
      setLoading(false);
    }
  };

  // Show loading while checking authentication
  if (checkingAuth) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid rgba(255,255,255,0.3)',
            borderTop: '4px solid white',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 16px'
          }}></div>
          <p>Checking authentication...</p>
          <style>
            {`
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
            `}
          </style>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      {/* Hero Section - Landing Page Features */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '60px',
        maxWidth: '1200px',
        width: '100%',
        alignItems: 'center'
      }}>
        {/* Left Side - Hero Content */}
        <div style={{ color: 'white' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '32px',
            gap: '16px'
          }}>
            <span style={{ fontSize: '56px' }}>📅</span>
            <h1 style={{ 
              fontSize: '48px', 
              margin: 0, 
              fontWeight: 'bold',
              textShadow: '0 2px 4px rgba(0,0,0,0.3)'
            }}>
              KairoCal
            </h1>
          </div>
          
          <h2 style={{ 
            fontSize: '32px', 
            marginBottom: '24px', 
            fontWeight: 'normal',
            lineHeight: '1.2'
          }}>
            AI-Powered Smart Calendar
          </h2>
          
          <p style={{ 
            fontSize: '20px', 
            marginBottom: '40px', 
            opacity: 0.9,
            lineHeight: '1.6'
          }}>
            Transform how you manage time with intelligent scheduling, natural language processing, and automatic conflict detection.
          </p>

          {/* Feature List */}
          <div style={{ marginBottom: '40px' }}>
            <div style={{
              display: 'grid',
              gap: '16px'
            }}>
              {[
                { icon: '🤖', text: 'Natural language event creation' },
                { icon: '⚡', text: 'Smart conflict detection' },
                { icon: '🔔', text: 'Intelligent notifications' },
                { icon: '☁️', text: 'Cloud-native architecture' }
              ].map((feature, index) => (
                <div key={index} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px 20px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  borderRadius: '12px',
                  backdropFilter: 'blur(10px)'
                }}>
                  <span style={{ fontSize: '24px' }}>{feature.icon}</span>
                  <span style={{ fontSize: '16px', fontWeight: '500' }}>{feature.text}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '24px',
            marginTop: '40px'
          }}>
            {[
              { number: '10K+', label: 'Events Scheduled' },
              { number: '99.9%', label: 'Uptime' },
              { number: '< 1s', label: 'Response Time' }
            ].map((stat, index) => (
              <div key={index} style={{ textAlign: 'center' }}>
                <div style={{ 
                  fontSize: '24px', 
                  fontWeight: 'bold',
                  marginBottom: '4px'
                }}>
                  {stat.number}
                </div>
                <div style={{ 
                  fontSize: '14px', 
                  opacity: 0.8 
                }}>
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side - Login Card */}
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '48px',
          boxShadow: '0 25px 50px rgba(0, 0, 0, 0.15)',
          textAlign: 'center',
          maxWidth: '450px',
          width: '100%',
          justifySelf: 'center'
        }}>
          {/* Login Header */}
          <div style={{ marginBottom: '32px' }}>
            <div style={{
              width: '80px',
              height: '80px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 24px',
              color: 'white',
              fontSize: '32px'
            }}>
              📅
            </div>
            
            <h1 style={{
              fontSize: '28px',
              fontWeight: 'bold',
              color: '#1f2937',
              margin: '0 0 8px 0'
            }}>
              Welcome Back
            </h1>
            <p style={{
              color: '#6b7280',
              fontSize: '16px',
              margin: 0
            }}>
              Sign in to access your smart calendar
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div style={{
              backgroundColor: '#fee2e2',
              border: '1px solid #fecaca',
              color: '#dc2626',
              padding: '16px',
              borderRadius: '12px',
              marginBottom: '24px',
              fontSize: '14px',
              textAlign: 'left'
            }}>
              <strong>⚠️ Authentication Error</strong>
              <br />
              {error}
            </div>
          )}

          {/* Login Button */}
          <button
            onClick={handleLogin}
            disabled={loading}
            style={{
              width: '100%',
              padding: '16px 24px',
              backgroundColor: loading ? '#9ca3af' : '#4f46e5',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s',
              marginBottom: '24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '12px',
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.4)'
            }}
            onMouseOver={(e) => !loading && (e.target.style.backgroundColor = '#4338ca')}
            onMouseOut={(e) => !loading && (e.target.style.backgroundColor = '#4f46e5')}
          >
            {loading ? (
              <>
                <div style={{
                  width: '20px',
                  height: '20px',
                  border: '2px solid rgba(255,255,255,0.3)',
                  borderTop: '2px solid white',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite'
                }}></div>
                Signing in...
              </>
            ) : (
              <>
                🔐 Sign in with AWS Cognito
              </>
            )}
          </button>

          {/* Divider */}
          <div style={{
            position: 'relative',
            margin: '24px 0',
            textAlign: 'center'
          }}>
            <div style={{
              height: '1px',
              background: '#e5e7eb'
            }}></div>
            <span style={{
              position: 'absolute',
              top: '-10px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'white',
              padding: '0 16px',
              color: '#6b7280',
              fontSize: '14px'
            }}>
              Coming Soon
            </span>
          </div>

          {/* Social Login Buttons (Disabled) */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <button
              disabled
              style={{
                width: '100%',
                padding: '12px 24px',
                backgroundColor: '#f9fafb',
                color: '#9ca3af',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                fontSize: '14px',
                cursor: 'not-allowed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              🔗 Continue with Google
            </button>
            
            <button
              disabled
              style={{
                width: '100%',
                padding: '12px 24px',
                backgroundColor: '#f9fafb',
                color: '#9ca3af',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                fontSize: '14px',
                cursor: 'not-allowed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              🔗 Continue with Microsoft
            </button>
          </div>

          {/* Footer */}
          <div style={{
            marginTop: '32px',
            paddingTop: '24px',
            borderTop: '1px solid #f3f4f6',
            textAlign: 'center'
          }}>
            <p style={{
              fontSize: '12px',
              color: '#9ca3af',
              margin: 0
            }}>
              By signing in, you agree to our{' '}
              <a href="#" style={{ color: '#4f46e5', textDecoration: 'none' }}>Terms</a>
              {' '}and{' '}
              <a href="#" style={{ color: '#4f46e5', textDecoration: 'none' }}>Privacy Policy</a>
            </p>
          </div>
        </div>
      </div>

      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          
          @media (max-width: 768px) {
            .hero-grid {
              grid-template-columns: 1fr !important;
              gap: 40px !important;
              text-align: center !important;
            }
          }
        `}
      </style>
    </div>
  );
};

export default AuthPage;