import React, { useState } from 'react';
import FrontendDiagnostics from '../../components/test/FrontendDiagnostics';
import VoiceCommandCenter from '../../components/voice/VoiceCommandCenter';
import AnalyticsPanel from '../../components/analytics/AnalyticsPanel';
import MiniCalendar from '../../components/calendar/MiniCalendar';
import ConflictDetectionPanel from '../../components/conflicts/ConflictDetectionPanel';

const DebugDashboard: React.FC = () => {
  const [activeTest, setActiveTest] = useState<string | null>(null);

  const renderTestComponent = () => {
    switch (activeTest) {
      case 'voice':
        return (
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold mb-4">🎤 Voice Command Center Test</h3>
            <VoiceCommandCenter />
          </div>
        );
      case 'analytics':
        return (
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold mb-4">📊 Analytics Panel Test</h3>
            <AnalyticsPanel />
          </div>
        );
      case 'calendar':
        return (
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold mb-4">📅 Mini Calendar Test</h3>
            <MiniCalendar events={[]} />
          </div>
        );
      case 'conflicts':
        return (
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold mb-4">⚡ Conflict Detection Test</h3>
            <ConflictDetectionPanel />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen">
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <span className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mr-3">
            <span className="text-white font-bold text-sm">K</span>
          </span>
          KairoCal - Debug Mode
        </h1>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-yellow-800 font-medium">🔧 Diagnostic Mode Active</p>
          <p className="text-yellow-700 text-sm mt-1">
            This is a temporary debug dashboard to identify and fix frontend issues step by step.
            We'll restore the full dashboard once all issues are resolved.
          </p>
        </div>
      </div>

      <FrontendDiagnostics />

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">🧪 Component Test Area</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <button 
            className={`p-4 border rounded-lg text-left transition-colors ${
              activeTest === 'voice' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTest(activeTest === 'voice' ? null : 'voice')}
          >
            <div className="font-medium">🎤 Voice Component</div>
            <div className="text-sm text-gray-600">Test voice recognition and BERT</div>
          </button>
          <button 
            className={`p-4 border rounded-lg text-left transition-colors ${
              activeTest === 'analytics' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTest(activeTest === 'analytics' ? null : 'analytics')}
          >
            <div className="font-medium">📊 Analytics Component</div>
            <div className="text-sm text-gray-600">Test BERT performance data</div>
          </button>
          <button 
            className={`p-4 border rounded-lg text-left transition-colors ${
              activeTest === 'calendar' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTest(activeTest === 'calendar' ? null : 'calendar')}
          >
            <div className="font-medium">📅 Calendar Component</div>
            <div className="text-sm text-gray-600">Test calendar display</div>
          </button>
          <button 
            className={`p-4 border rounded-lg text-left transition-colors ${
              activeTest === 'conflicts' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTest(activeTest === 'conflicts' ? null : 'conflicts')}
          >
            <div className="font-medium">⚡ Conflict Detection</div>
            <div className="text-sm text-gray-600">Test AI conflict resolution</div>
          </button>
        </div>
        
        {activeTest && (
          <div className="mb-4">
            <button
              onClick={() => setActiveTest(null)}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded transition-colors"
            >
              ← Back to Component Selection
            </button>
          </div>
        )}
      </div>

      {renderTestComponent()}

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">🎯 Next Steps</h2>
        <div className="space-y-3 text-sm">
          <div className="flex items-start space-x-3">
            <span className="text-blue-600 font-bold">1.</span>
            <div>
              <p className="font-medium">Check diagnostics above - Should show 100% healthy ✅</p>
              <p className="text-gray-600">All API connectivity and browser features working</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-blue-600 font-bold">2.</span>
            <div>
              <p className="font-medium">Test components individually using buttons above</p>
              <p className="text-gray-600">Click each component button to verify functionality</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-blue-600 font-bold">3.</span>
            <div>
              <p className="font-medium">Ready to restore full dashboard!</p>
              <p className="text-gray-600">Once components work, we can switch back to the complete interface</p>
              <div className="mt-2">
                <button 
                  onClick={() => window.location.href = '/dashboard'}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                >
                  🚀 Switch to Full Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DebugDashboard;
