import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import AuthForm from '../../components/auth/AuthForm';

const AuthPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Auth Form */}
      <div className="flex-1 flex items-center justify-center bg-white px-8 py-12">
        <motion.div
          className="w-full max-w-md"
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* KairoCal Logo */}
          <div className="mb-8">
            <div className="flex items-center mb-8">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-xl">K.</span>
              </div>
            </div>
          </div>

          <AuthForm onSuccess={() => console.log('Authentication successful!')} />

          <div className="mt-8 pt-6">
            <button
              onClick={() => navigate('/')}
              className="text-gray-500 hover:text-gray-700 text-sm"
            >
              ← Back to Home
            </button>
          </div>
        </motion.div>
      </div>

      {/* Right Side - Marketing Content */}
      <div className="flex-1 relative bg-gray-50 flex items-center justify-center overflow-hidden">
        {/* Abstract Background Shapes */}
        <div className="absolute inset-0">
          {/* Blue blob - top */}
          <div className="absolute top-0 right-20 w-64 h-64 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full opacity-80 transform rotate-12"></div>
          
          {/* Coral blob - top right */}
          <div className="absolute top-20 right-0 w-48 h-48 bg-gradient-to-br from-orange-400 to-pink-500 rounded-full opacity-70 transform -rotate-45"></div>
          
          {/* Purple blob - bottom right */}
          <div className="absolute bottom-0 right-0 w-72 h-72 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full opacity-75 transform rotate-45"></div>
          
          {/* Teal blob - bottom center */}
          <div className="absolute bottom-20 left-1/2 w-40 h-40 bg-gradient-to-br from-teal-400 to-cyan-500 rounded-full opacity-80 transform -translate-x-1/2"></div>
          
          {/* Pink blob - center left */}
          <div className="absolute top-1/2 left-10 w-52 h-52 bg-gradient-to-br from-pink-400 to-red-500 rounded-full opacity-70 transform -translate-y-1/2 rotate-12"></div>
        </div>

        {/* Content */}
        <motion.div
          className="relative z-10 text-center px-12"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <h1 className="text-5xl font-bold text-gray-900 mb-4 leading-tight">
            Revolutionizing the way
            <br />
            <span className="bg-gradient-to-r from-pink-500 to-orange-500 bg-clip-text text-transparent">
              the world schedules
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 mt-6 max-w-md mx-auto">
            Experience AI-powered scheduling with voice commands, intelligent conflict detection, and seamless calendar management.
          </p>
        </motion.div>

        {/* Floating Animation for Blobs */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-0 right-20 w-64 h-64 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full opacity-80 animate-bounce"></div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
