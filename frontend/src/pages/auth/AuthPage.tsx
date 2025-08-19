import React, { useState, useEffect } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import AuthForm from '../../components/auth/AuthForm';

const AuthPage: React.FC = () => {
  const navigate = useNavigate();
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const { scrollYProgress } = useScroll();
  
  // Advanced scroll-based transforms
  const heroY = useTransform(scrollYProgress, [0, 1], ['0%', '50%']);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.3], [1, 0]);

  // Mouse tracking for interactive elements
  useEffect(() => {
    let animationFrame: number;
    const handleMouseMove = (e: MouseEvent) => {
      animationFrame = requestAnimationFrame(() => {
        setMousePosition({ x: e.clientX, y: e.clientY });
      });
    };
    
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
    };
  }, []);

  // Real-time stats (matching landing page data)
  const [stats] = useState({
    eventsProcessed: 1247,
    aiAccuracy: 87.3,
    voiceCommands: 892,
    conflictsResolved: 156
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden">
      {/* Advanced Animated Background (matching landing page) */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5"></div>
          {/* Dot pattern */}
          <div className="absolute inset-0 opacity-20 dot-pattern"></div>
        </div>
        
        {/* Floating orbs that follow mouse */}
        <motion.div
          className="absolute w-96 h-96 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full blur-3xl"
          animate={{
            x: mousePosition.x * 0.02,
            y: mousePosition.y * 0.02,
          }}
          transition={{ type: "spring", damping: 30 }}
        />
        <motion.div
          className="absolute top-1/2 right-0 w-64 h-64 bg-gradient-to-r from-indigo-500/20 to-pink-500/20 rounded-full blur-3xl"
          animate={{
            x: -mousePosition.x * 0.01,
            y: -mousePosition.y * 0.01,
          }}
          transition={{ type: "spring", damping: 40 }}
        />
      </div>

      {/* Navigation with glassmorphism (matching landing page) */}
      <nav className="relative z-50 flex justify-between items-center px-6 py-4 bg-white/10 backdrop-blur-md border-b border-white/10">
        <motion.div 
          className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent cursor-pointer"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          onClick={() => navigate('/')}
        >
          KairoCal
        </motion.div>
        
        {/* Live stats in nav */}
        <motion.div 
          className="hidden md:flex items-center gap-6 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-gray-300">{stats.eventsProcessed.toLocaleString()} events processed</span>
          </div>
          <div className="text-gray-400">|</div>
          <div className="text-gray-300">{stats.aiAccuracy}% AI accuracy</div>
        </motion.div>

        <motion.button
          className="text-gray-300 hover:text-white text-sm transition-colors"
          onClick={() => navigate('/')}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          ← Back to Home
        </motion.button>
      </nav>

      <div className="flex min-h-[calc(100vh-80px)]">
        {/* Left Side - Auth Form with advanced styling */}
        <div className="flex-1 flex items-center justify-center px-8 py-12 relative z-10">
          <motion.div
            className="w-full max-w-md relative"
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            {/* Glassmorphism container for auth form */}
            <div className="relative p-8 bg-white/10 backdrop-blur-xl rounded-3xl border border-white/20 shadow-2xl shadow-purple-500/10">
              {/* Animated border */}
              <motion.div
                className="absolute inset-0 rounded-3xl border-2 border-transparent"
                animate={{
                  borderColor: ["rgba(59, 130, 246, 0)", "rgba(59, 130, 246, 0.3)", "rgba(59, 130, 246, 0)"]
                }}
                transition={{ duration: 3, repeat: Infinity }}
              />

              {/* KairoCal Logo with advanced styling */}
              <div className="mb-8 text-center">
                <motion.div 
                  className="flex items-center justify-center mb-6"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", damping: 10, stiffness: 100, delay: 0.2 }}
                >
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/25">
                    <span className="text-white font-bold text-2xl">K.</span>
                  </div>
                </motion.div>
                
                {/* AI Badge */}
                <motion.div
                  className="inline-flex items-center gap-2 px-3 py-1 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full border border-blue-500/30 mb-4"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></div>
                  <span className="text-xs font-medium text-blue-300">Powered by Advanced AI</span>
                </motion.div>
              </div>

              <AuthForm onSuccess={() => console.log('Authentication successful!')} />
            </div>

            {/* Floating elements around the form */}
            <motion.div
              className="absolute -top-4 -right-4 w-8 h-8 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full opacity-60"
              animate={{ y: [-10, 10, -10] }}
              transition={{ duration: 3, repeat: Infinity }}
            />
            <motion.div
              className="absolute -bottom-6 -left-6 w-6 h-6 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full opacity-50"
              animate={{ y: [10, -10, 10] }}
              transition={{ duration: 4, repeat: Infinity }}
            />
          </motion.div>
        </div>

        {/* Right Side - Advanced Marketing Content */}
        <div className="flex-1 relative flex items-center justify-center overflow-hidden">
          {/* Enhanced Background with parallax */}
          <motion.div 
            className="absolute inset-0"
            style={{ y: heroY, opacity: heroOpacity }}
          >
            {/* Animated gradient orbs */}
            <motion.div 
              className="absolute top-10 right-20 w-64 h-64 bg-gradient-to-br from-blue-400/30 to-blue-600/30 rounded-full blur-2xl"
              animate={{ 
                scale: [1, 1.2, 1],
                rotate: [0, 360],
                x: [0, 20, 0],
                y: [0, -20, 0]
              }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            />
            
            <motion.div 
              className="absolute top-32 right-0 w-48 h-48 bg-gradient-to-br from-purple-400/30 to-pink-500/30 rounded-full blur-2xl"
              animate={{ 
                scale: [1, 0.8, 1],
                rotate: [360, 0],
                x: [0, -30, 0],
                y: [0, 40, 0]
              }}
              transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
            />
            
            <motion.div 
              className="absolute bottom-10 right-10 w-80 h-80 bg-gradient-to-br from-indigo-400/20 to-purple-600/20 rounded-full blur-3xl"
              animate={{ 
                scale: [1, 1.3, 1],
                rotate: [0, -360],
                x: [0, -40, 0],
                y: [0, 20, 0]
              }}
              transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
            />
            
            <motion.div 
              className="absolute bottom-32 left-1/2 w-40 h-40 bg-gradient-to-br from-teal-400/30 to-cyan-500/30 rounded-full blur-xl"
              animate={{ 
                scale: [1, 1.1, 1],
                x: [0, 50, 0],
                y: [0, -30, 0]
              }}
              transition={{ duration: 12, repeat: Infinity }}
            />
            
            <motion.div 
              className="absolute top-1/2 left-10 w-52 h-52 bg-gradient-to-br from-pink-400/25 to-red-500/25 rounded-full blur-2xl"
              animate={{ 
                scale: [1, 0.9, 1],
                rotate: [0, 180, 360],
                y: [0, 60, 0]
              }}
              transition={{ duration: 18, repeat: Infinity }}
            />
          </motion.div>

          {/* Main Content with advanced animations */}
          <motion.div
            className="relative z-10 text-center px-12 max-w-2xl"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <motion.h1 
              className="text-6xl font-bold mb-6 leading-tight"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
            >
              <span className="bg-gradient-to-r from-white via-blue-200 to-purple-200 bg-clip-text text-transparent">
                Revolutionizing the way
              </span>
              <br />
              <span className="bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
                the world schedules
              </span>
            </motion.h1>
            
            <motion.p 
              className="text-xl text-gray-300 mb-8 max-w-lg mx-auto leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.7 }}
            >
              Experience AI-powered scheduling with <span className="text-blue-400 font-semibold">BERT neural networks</span>, 
              voice commands, intelligent conflict detection, and seamless calendar management.
            </motion.p>
          </motion.div>

          {/* Geometric floating elements */}
          <motion.div
            className="absolute top-20 right-40 w-3 h-3 bg-blue-400 rounded-full opacity-60"
            animate={{ 
              y: [-10, 10, -10],
              opacity: [0.6, 1, 0.6]
            }}
            transition={{ duration: 3, repeat: Infinity }}
          />
          <motion.div
            className="absolute bottom-40 right-20 w-2 h-2 bg-purple-400 rounded-full opacity-50"
            animate={{ 
              y: [10, -10, 10],
              x: [-5, 5, -5],
              opacity: [0.5, 0.8, 0.5]
            }}
            transition={{ duration: 4, repeat: Infinity }}
          />
          <motion.div
            className="absolute top-1/2 right-10 w-4 h-4 bg-pink-400 rounded-full opacity-40"
            animate={{ 
              scale: [1, 1.2, 1],
              opacity: [0.4, 0.7, 0.4]
            }}
            transition={{ duration: 2.5, repeat: Infinity }}
          />
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
