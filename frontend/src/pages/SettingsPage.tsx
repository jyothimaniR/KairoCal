import React, { useState } from 'react';
import {
  UserIcon,
  Cog6ToothIcon,
  ArrowDownTrayIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import { userService } from '../stores/userStore';

// Safe types - no complex interfaces
interface AppPreferences {
  default_event_duration: 'smart' | 30 | 60 | 90 | 120;
  voice_recognition_enabled: boolean;
}

const SettingsPage: React.FC = () => {
  // Load user data from service
  const [userProfile, setUserProfile] = useState(() => userService.getUser());

  // Load preferences from localStorage or use defaults
  const [preferences, setPreferences] = useState<AppPreferences>(() => {
    try {
      const saved = localStorage.getItem('user-preferences');
      if (saved) {
        const parsed = JSON.parse(saved);
        return {
          default_event_duration: parsed.default_event_duration || 'smart',
          voice_recognition_enabled: parsed.voice_recognition_enabled !== undefined ? parsed.voice_recognition_enabled : true
        };
      }
    } catch (error) {
      console.log('Using default preferences');
    }
    return {
      default_event_duration: 'smart',
      voice_recognition_enabled: true
    };
  });

  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  // Real save function that updates the user service
  const handleSaveProfile = async () => {
    setIsLoading(true);
    
    // Update user service (which updates localStorage and notifies other components)
    userService.updateUser({
      full_name: userProfile.full_name
    });
    
    // Simulate API delay
    setTimeout(() => {
      setIsLoading(false);
      setSuccessMessage('Profile updated successfully! Changes will appear in the header.');
      setTimeout(() => setSuccessMessage(''), 3000);
    }, 1000);
  };

  const handleSavePreferences = async () => {
    setIsLoading(true);
    
    // Save preferences to localStorage for API consumption
    try {
      localStorage.setItem('user-preferences', JSON.stringify(preferences));
      console.log('💾 Saved preferences:', preferences);
    } catch (error) {
      console.error('Failed to save preferences:', error);
    }
    
    // Simulate API call delay  
    setTimeout(() => {
      setIsLoading(false);
      setSuccessMessage('Preferences saved successfully! Voice events will now use your duration setting.');
      setTimeout(() => setSuccessMessage(''), 3000);
    }, 1000);
  };

  // Simple export function - no complex data processing
  const handleExportData = () => {
    const exportData = {
      profile: userProfile,
      preferences: preferences,
      export_date: new Date().toISOString(),
      version: '1.0'
    };

    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `kairocal-settings-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setSuccessMessage('Data exported successfully!');
    setTimeout(() => setSuccessMessage(''), 3000);
  };

  return (
    <div className="min-h-full bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="mt-2 text-gray-600">Manage your account preferences and app settings</p>
        </div>

        {/* Success Message */}
        {successMessage && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4"
          >
            <div className="flex items-center">
              <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
              <span className="text-green-800">{successMessage}</span>
            </div>
          </motion.div>
        )}

        <div className="space-y-8">
          {/* User Profile Section */}
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center">
                <UserIcon className="h-6 w-6 text-gray-500 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">User Profile</h2>
              </div>
            </div>
            <div className="px-6 py-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Full Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    value={userProfile.full_name}
                    onChange={(e) => setUserProfile(prev => ({ ...prev, full_name: e.target.value }))}
                    placeholder="Enter your full name"
                    title="Full Name"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>

                {/* Email (Read-only) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={userProfile.email}
                    disabled
                    title="Email Address"
                    placeholder="Email address"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">Email cannot be changed</p>
                </div>

                {/* Account Status (Display only) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Account Status
                  </label>
                  <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                    userProfile.account_status === 'active'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    <div className={`w-2 h-2 rounded-full mr-2 ${
                      userProfile.account_status === 'active' ? 'bg-green-500' : 'bg-red-500'
                    }`}></div>
                    {userProfile.account_status === 'active' ? 'Active' : 'Inactive'}
                  </div>
                </div>
              </div>

              <div className="mt-6">
                <button
                  onClick={handleSaveProfile}
                  disabled={isLoading}
                  className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Saving...' : 'Save Profile'}
                </button>
              </div>
            </div>
          </div>

          {/* App Preferences Section */}
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center">
                <Cog6ToothIcon className="h-6 w-6 text-gray-500 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">App Preferences</h2>
              </div>
            </div>
            <div className="px-6 py-6">
              <div className="grid grid-cols-1 gap-6">
                {/* Default Event Duration */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Event Duration Behavior
                  </label>
                  <p className="text-xs text-gray-500 mb-4">
                    Choose how event durations are determined when not explicitly specified
                  </p>
                  
                  {/* Smart Duration Option */}
                  <div className="mb-4">
                    <label className="flex items-start space-x-3 p-4 border-2 border-purple-200 rounded-lg bg-gradient-to-r from-purple-50 to-blue-50 cursor-pointer hover:border-purple-300 transition-colors">
                      <input
                        type="radio"
                        name="duration_mode"
                        value="smart"
                        checked={preferences.default_event_duration === 'smart'}
                        onChange={() => setPreferences(prev => ({ 
                          ...prev, 
                          default_event_duration: 'smart' as const
                        }))}
                        className="mt-1 w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                      />
                      <div className="flex-1">
                        <div className="flex items-center">
                          <span className="font-medium text-gray-900">🧠 Smart Duration Detection</span>
                          <span className="ml-2 px-2 py-1 text-xs bg-purple-100 text-purple-700 rounded-full">Recommended</span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">
                          Intelligently determines event duration based on event type (meetings=60min, calls=30min, yoga classes=75min, etc.)
                        </p>
                      </div>
                    </label>
                  </div>

                  {/* Fixed Duration Options */}
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-gray-700">Or choose a fixed duration:</p>
                    
                    {[
                      { value: 30, label: '30 minutes' },
                      { value: 60, label: '1 hour' },
                      { value: 90, label: '1 hour 30 minutes' },
                      { value: 120, label: '2 hours' }
                    ].map((option) => (
                      <label key={option.value} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                        <input
                          type="radio"
                          name="duration_mode"
                          value={option.value}
                          checked={preferences.default_event_duration === option.value}
                          onChange={(e) => setPreferences(prev => ({ 
                            ...prev, 
                            default_event_duration: parseInt(e.target.value) as 30 | 60 | 90 | 120
                          }))}
                          className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                        />
                        <span className="text-gray-700">{option.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Voice Recognition Toggle */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Voice Recognition
                  </label>
                  <div className="flex items-center">
                    <button
                      onClick={() => setPreferences(prev => ({ 
                        ...prev, 
                        voice_recognition_enabled: !prev.voice_recognition_enabled 
                      }))}
                      title={`${preferences.voice_recognition_enabled ? 'Disable' : 'Enable'} voice recognition`}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        preferences.voice_recognition_enabled ? 'bg-purple-600' : 'bg-gray-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          preferences.voice_recognition_enabled ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                    <span className="ml-3 text-sm text-gray-700">
                      {preferences.voice_recognition_enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-6">
                <button
                  onClick={handleSavePreferences}
                  disabled={isLoading}
                  className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Saving...' : 'Save Preferences'}
                </button>
              </div>
            </div>
          </div>

          {/* Data Management Section */}
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center">
                <ArrowDownTrayIcon className="h-6 w-6 text-gray-500 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">Data Management</h2>
              </div>
            </div>
            <div className="px-6 py-6">
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-2">Export Your Data</h3>
                  <p className="text-sm text-gray-600 mb-4">
                    Download a copy of your profile and preferences data as a JSON file.
                  </p>
                  <button
                    onClick={handleExportData}
                    className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
                  >
                    Export Data
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
