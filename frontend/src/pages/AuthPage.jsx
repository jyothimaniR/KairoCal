import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, getCurrentAuthUser } from '../services/authService';

const AuthPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const authData = await getCurrentAuthUser();
        if (authData) {
          navigate('/dashboard', { replace: true });
        }
      } catch (error) {
        // User not authenticated, do nothing
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
      await login();
    } catch (error) {
      setError('Login failed. Please try again.');
      setLoading(false);
    }
  };

  if (checkingAuth) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-blue-400">
        <div className="text-center text-white">
          <div className="w-10 h-10 border-4 border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-lg font-medium">Checking authentication...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-blue-400 px-4">
      <div className="w-full max-w-md bg-white/90 rounded-3xl shadow-2xl p-8 md:p-12 flex flex-col items-center">
        <div className="mb-8 flex flex-col items-center">
          <div className="w-16 h-16 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-2xl flex items-center justify-center shadow-lg mb-4">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="10" width="30" height="25" rx="5" fill="#fff" fillOpacity="0.9"/>
              <rect x="5" y="10" width="30" height="25" rx="5" stroke="#a78bfa" strokeWidth="2"/>
              <rect x="12" y="5" width="4" height="8" rx="2" fill="#a78bfa"/>
              <rect x="24" y="5" width="4" height="8" rx="2" fill="#a78bfa"/>
              <rect x="10" y="18" width="4" height="4" rx="2" fill="#a78bfa"/>
              <rect x="18" y="18" width="4" height="4" rx="2" fill="#a78bfa"/>
              <rect x="26" y="18" width="4" height="4" rx="2" fill="#a78bfa"/>
            </svg>
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-2 text-center tracking-tight">KairoCal</h1>
          <h2 className="text-lg md:text-xl font-semibold text-indigo-700 mb-4 text-center uppercase tracking-wider">AI-Powered Smart Calendar</h2>
        </div>
        <p className="text-gray-600 text-center mb-8 text-base md:text-lg leading-relaxed">
          Transform how you manage time with intelligent scheduling,<br />
          natural language processing, and automatic conflict detection.
        </p>
        {error && (
          <div className="mb-4 w-full p-3 bg-red-50 border border-red-200 text-red-700 rounded">
            <p className="font-semibold">Authentication Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}
        <button
          onClick={handleLogin}
          disabled={loading}
          className={`w-full py-4 px-8 text-lg font-bold rounded-full shadow-md transition-all duration-200 flex items-center justify-center gap-3
            ${loading ? 'bg-gray-400 text-white cursor-not-allowed' : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:scale-105 hover:shadow-lg focus:outline-none focus:ring-4 focus:ring-indigo-300'}`}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              Starting...
            </span>
          ) : (
            'Get Started'
          )}
        </button>
      </div>
    </div>
  );
};

export default AuthPage;
