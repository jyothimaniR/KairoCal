import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline';
import { motion, AnimatePresence } from 'framer-motion';
import { userService } from '../../stores/userStore';

interface UserButtonProps {
  isVoiceHealthy?: boolean;
}

const UserButton: React.FC<UserButtonProps> = ({ 
  isVoiceHealthy = true
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [userData, setUserData] = useState(() => userService.getUser());
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Listen for user updates
  useEffect(() => {
    const handleUserUpdate = (event: CustomEvent) => {
      setUserData(event.detail);
    };

    window.addEventListener('user-updated', handleUserUpdate as EventListener);
    return () => window.removeEventListener('user-updated', handleUserUpdate as EventListener);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Get user initials for avatar
  const getInitials = (name: string): string => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const handleSignOut = () => {
    // Simple sign out - just reload to landing page
    window.location.href = '/';
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* User Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
      >
        {/* User Avatar */}
        <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
          <span className="text-white font-medium text-sm">
            {getInitials(userData.full_name)}
          </span>
        </div>
        
        {/* User Info */}
        <div className="text-left">
          <div className="text-sm font-medium text-gray-700">{userData.full_name}</div>
        </div>
        
        {/* Dropdown Arrow */}
        <ChevronDownIcon 
          className={`h-4 w-4 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
        />
      </button>

      {/* Dropdown Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -10 }}
            transition={{ duration: 0.1 }}
            className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
          >
            {/* User Info Header */}
            <div className="px-4 py-3 border-b border-gray-100">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-medium">
                    {getInitials(userData.full_name)}
                  </span>
                </div>
                <div>
                  <div className="font-medium text-gray-900">{userData.full_name}</div>
                  <div className="text-sm text-gray-500">{userData.email}</div>
                </div>
              </div>
              
              {/* Status Indicator */}
              <div className="mt-2">
                <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs ${
                  isVoiceHealthy 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-red-100 text-red-700'
                }`}>
                  <div className={`w-2 h-2 rounded-full mr-1 ${
                    isVoiceHealthy ? 'bg-green-500' : 'bg-red-500'
                  }`}></div>
                  {isVoiceHealthy ? 'System Online' : 'System Offline'}
                </div>
              </div>
            </div>

            {/* Menu Items */}
            <div className="py-2">
              {/* Settings */}
              <Link
                to="/settings"
                onClick={() => setIsOpen(false)}
                className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <Cog6ToothIcon className="h-4 w-4 mr-3 text-gray-500" />
                Settings
              </Link>

              {/* Profile (placeholder for future) */}
              <button
                onClick={() => setIsOpen(false)}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <UserIcon className="h-4 w-4 mr-3 text-gray-500" />
                Profile
              </button>
            </div>

            {/* Divider */}
            <div className="border-t border-gray-100"></div>

            {/* Sign Out */}
            <div className="py-2">
              <button
                onClick={handleSignOut}
                className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                <ArrowRightOnRectangleIcon className="h-4 w-4 mr-3 text-red-500" />
                Sign Out
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default UserButton;
