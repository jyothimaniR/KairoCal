import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
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

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [voiceApiHealth, setVoiceApiHealth] = useState(false);
  const location = useLocation();

  console.log('🏗️ Layout component rendering with location:', location.pathname);

  // Check voice API health on component mount
  useEffect(() => {
    checkVoiceApiHealth();
  }, []);

  const checkVoiceApiHealth = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8001/health');
      setVoiceApiHealth(response.ok);
    } catch (error) {
      setVoiceApiHealth(false);
    }
  };

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
          <div className="text-xs font-medium text-gray-900 mb-3">🤖 AI Status</div>
          <div className="space-y-2 text-xs">
            <div className={`flex items-center ${voiceApiHealth ? 'text-green-600' : 'text-red-600'}`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${voiceApiHealth ? 'bg-green-500' : 'bg-red-500'}`}></div>
              BERT {voiceApiHealth ? 'Online' : 'Offline'}
            </div>
            <div className={`flex items-center ${voiceApiHealth ? 'text-green-600' : 'text-red-600'}`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${voiceApiHealth ? 'bg-green-500' : 'bg-red-500'}`}></div>
              Voice {voiceApiHealth ? 'Ready' : 'Unavailable'}
            </div>
            <div className="flex items-center text-blue-600">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
              Sync Active
            </div>
            <div className="text-xs text-gray-500 mt-2">
              📊 12 events
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
                  type="text"
                  placeholder="What's on your mind?"
                  className="w-full pl-10 pr-10 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
                <button className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <MicrophoneIcon className="h-4 w-4 text-purple-500" />
                </button>
              </div>
            </div>

            {/* Right Side */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3 text-sm">
                <button className="p-2 hover:bg-gray-100 rounded-lg relative">
                  <BellIcon className="h-5 w-5 text-gray-600" />
                  <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full text-xs text-white flex items-center justify-center"></span>
                </button>
                <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg ${voiceApiHealth ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                  <MicrophoneIcon className="h-4 w-4" />
                  <span className="text-xs font-medium">
                    {voiceApiHealth ? 'Voice Ready' : 'Voice Offline'}
                  </span>
                </div>
                <span className="text-purple-600 font-medium">📊 87%</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
                <span className="text-sm font-medium text-gray-700">John Doe</span>
              </div>
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
