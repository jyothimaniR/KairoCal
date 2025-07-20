import React from 'react';
import { logout } from '../services/authService';

const Dashboard = () => {
  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold text-blue-600">KairoCal</h1>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🎉 Welcome to KairoCal
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            You are successfully authenticated via AWS Cognito Managed Login
          </p>
          
          <div className="bg-white rounded-lg shadow p-6 max-w-md mx-auto">
            <h2 className="text-xl font-semibold mb-4">Coming Soon</h2>
            <ul className="text-left space-y-2 text-gray-600">
              <li>📅 Smart Calendar Integration</li>
              <li>🤖 AI-Powered Event Creation</li>
              <li>🔔 Intelligent Notifications</li>
              <li>📱 Mobile Responsive Design</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;