import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  HomeIcon,
  CalendarIcon,
  MicrophoneIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  MagnifyingGlassIcon,
  Cog6ToothIcon,
  BellIcon,
} from '@heroicons/react/24/outline';
import { useVoice } from '../../hooks/useVoice';
import { useSystemHealth } from '../../hooks/useSystemHealth';
import { useDashboard } from '../../hooks/useDashboard';
import { useNotificationGenerator } from '../../hooks/useNotificationGenerator';
import UserButton from './UserButton';
import { NotificationDropdown } from '../notifications/NotificationDropdown';
// Import development helper in development mode
if (process.env.NODE_ENV === 'development') {
  import('../../utils/notificationDev');
}

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  // Use unified system health hook
  const { isVoiceHealthy, isBertHealthy, systemHealth } = useSystemHealth();
  // Get real event data for the indicator
  const { events, productivityMetrics } = useDashboard();
  // Generate notifications automatically
  useNotificationGenerator();
  const location = useLocation();
  const navigate = useNavigate();
  const { isListening, startListening, stopListening } = useVoice();
  const [headerQuery, setHeaderQuery] = useState('');

  console.log('🏗️ Layout component rendering with location:', location.pathname);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Calendar', href: '/calendar', icon: CalendarIcon },
    { name: 'Voice Hub', href: '/voice', icon: MicrophoneIcon },
    { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
    { name: 'Conflicts', href: '/conflicts', icon: ExclamationTriangleIcon },
    { name: 'Search', href: '/search', icon: MagnifyingGlassIcon },
    { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
  ];

  return (
    <div className="h-screen w-screen bg-gray-50 flex overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-sm border-r border-gray-200 flex flex-col flex-shrink-0">
        {/* Logo */}
        <div className="px-6 py-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">K</span>
            </div>
            <span className="text-xl font-semibold text-gray-900">KairoCal</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-6 py-6 space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                  isActive
                    ? 'bg-purple-50 text-purple-700 border border-purple-200'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* AI Status Panel */}
        <div className="px-6 py-4 border-t border-gray-200">
          <div className="text-xs font-medium text-gray-900 mb-3 flex items-center justify-between">
            <span>🤖 AI Status</span>
            <div className={`w-1.5 h-1.5 rounded-full ${systemHealth ? 'bg-green-400 animate-pulse' : 'bg-gray-400'}`}></div>
          </div>
          <div className="space-y-2 text-xs">
            <div className={`flex items-center ${isBertHealthy ? 'text-green-600' : 'text-red-600'}`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${isBertHealthy ? 'bg-green-500' : 'bg-red-500'}`}></div>
              BERT {isBertHealthy ? 'Online' : 'Offline'}
            </div>
            <div className={`flex items-center ${isVoiceHealthy ? 'text-green-600' : 'text-red-600'}`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${isVoiceHealthy ? 'bg-green-500' : 'bg-red-500'}`}></div>
              Voice {isVoiceHealthy ? 'Ready' : 'Unavailable'}
            </div>
            <div className={`flex items-center ${systemHealth ? 'text-blue-600' : 'text-gray-400'}`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${systemHealth ? 'bg-blue-500' : 'bg-gray-400'}`}></div>
              Sync {systemHealth ? 'Active' : 'Offline'}
            </div>
            <div className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-100">
              📊 {events.length} events
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4 flex-shrink-0">
          <div className="flex items-center justify-between">
            {/* Search Bar */}
            <div className="flex-1 max-w-md">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  id="global-search"
                  name="globalSearch"
                  type="text"
                  value={headerQuery}
                  onChange={(e) => setHeaderQuery(e.target.value)}
                  placeholder="Search for events or tasks"
                  autoComplete="off"
                  autoCorrect="off"
                  autoCapitalize="off"
                  spellCheck={false}
                  inputMode="search"
                  className="w-full pl-10 pr-10 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      navigate('/search', { state: { q: headerQuery } });
                    }
                  }}
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 transform -translate-y-1/2"
                  aria-label={isListening ? 'Stop voice input' : 'Start voice input'}
                  title={isListening ? 'Stop voice input' : 'Start voice input'}
                  onClick={async () => {
                    if (isListening) { stopListening(); return; }
                    try {
                      const res = await startListening();
                      if (res?.transcript) {
                        setHeaderQuery(res.transcript);
                        navigate('/search', { state: { q: res.transcript } });
                      }
                    } catch { /* ignore */ }
                  }}
                >
                  <MicrophoneIcon className={`h-4 w-4 ${isListening ? 'text-red-500' : 'text-purple-500'}`} />
                </button>
              </div>
            </div>

            {/* Right Side */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3 text-sm">
                <NotificationDropdown />
                <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg ${isVoiceHealthy ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                  <MicrophoneIcon className="h-4 w-4" />
                  <span className="text-xs font-medium">
                    {isVoiceHealthy ? 'Voice Ready' : 'Voice Offline'}
                  </span>
                </div>
                <div 
                  className="flex items-center space-x-1 px-3 py-1 bg-purple-50 text-purple-600 rounded-lg cursor-pointer hover:bg-purple-100 transition-colors"
                  title={`Productivity Score: ${productivityMetrics.currentScore || 0}% - Based on calendar efficiency and goal completion`}
                  onClick={() => navigate('/analytics')}
                >
                  <span className="text-xs font-medium">📊 {productivityMetrics.currentScore || 0}%</span>
                </div>
              </div>
              <UserButton 
                isVoiceHealthy={isVoiceHealthy}
              />
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-gray-50">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
