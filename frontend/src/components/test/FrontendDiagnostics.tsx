import React, { useEffect, useState } from 'react';

interface TestResult {
  test: string;
  status: 'success' | 'error' | 'loading';
  message: string;
  data?: any;
}

export const FrontendDiagnostics: React.FC = () => {
  const [tests, setTests] = useState<TestResult[]>([]);

  useEffect(() => {
    runDiagnostics();
  }, []);

  const addTest = (result: TestResult) => {
    setTests(prev => [...prev.filter(t => t.test !== result.test), result]);
  };

  const runDiagnostics = async () => {
    console.log('🔧 Running Frontend Diagnostics...');

    // Test 1: Basic API Connectivity
    addTest({ test: 'API Health Check', status: 'loading', message: 'Checking...' });
    try {
      const response = await fetch('http://127.0.0.1:8000/health');
      if (response.ok) {
        const data = await response.json();
        addTest({ 
          test: 'API Health Check', 
          status: 'success', 
          message: 'Backend is healthy', 
          data: data.status 
        });
      } else {
        addTest({ 
          test: 'API Health Check', 
          status: 'error', 
          message: `Failed: ${response.status}` 
        });
      }
    } catch (error) {
      addTest({ 
        test: 'API Health Check', 
        status: 'error', 
        message: `Network error: ${error}` 
      });
    }

    // Test 2: Events API
    addTest({ test: 'Events API', status: 'loading', message: 'Fetching events...' });
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/events?cognito_sub=frontend-test-user');
      if (response.ok) {
        const data = await response.json();
        addTest({ 
          test: 'Events API', 
          status: 'success', 
          message: `Found ${data.length} events`, 
          data: data.length 
        });
      } else {
        const errorText = await response.text();
        addTest({ 
          test: 'Events API', 
          status: 'error', 
          message: `Failed: ${response.status} - ${errorText.substring(0, 100)}` 
        });
      }
    } catch (error) {
      addTest({ 
        test: 'Events API', 
        status: 'error', 
        message: `Error: ${error}` 
      });
    }

    // Test 3: Browser Features
    addTest({ test: 'Web Speech API', status: 'loading', message: 'Checking browser support...' });
    const hasWebSpeech = ('webkitSpeechRecognition' in window) || ('SpeechRecognition' in window);
    addTest({ 
      test: 'Web Speech API', 
      status: hasWebSpeech ? 'success' : 'error', 
      message: hasWebSpeech ? 'Voice recognition supported' : 'Voice recognition not supported in this browser',
      data: hasWebSpeech
    });

    // Test 4: Local Storage
    addTest({ test: 'Local Storage', status: 'loading', message: 'Testing storage...' });
    try {
      localStorage.setItem('frontend_test', 'OK');
      const value = localStorage.getItem('frontend_test');
      localStorage.removeItem('frontend_test');
      addTest({ 
        test: 'Local Storage', 
        status: 'success', 
        message: 'Storage working', 
        data: value === 'OK' 
      });
    } catch (error) {
      addTest({ 
        test: 'Local Storage', 
        status: 'error', 
        message: `Storage error: ${error}` 
      });
    }

    // Test 5: Component Dependencies
    addTest({ test: 'React Dependencies', status: 'loading', message: 'Checking...' });
    try {
      // Test if core dependencies are loaded
      const hasFramerMotion = typeof window !== 'undefined' && 'motion' in (await import('framer-motion'));
      addTest({ 
        test: 'React Dependencies', 
        status: 'success', 
        message: 'Dependencies loaded successfully',
        data: { framerMotion: hasFramerMotion }
      });
    } catch (error) {
      addTest({ 
        test: 'React Dependencies', 
        status: 'error', 
        message: `Dependency error: ${error}` 
      });
    }
  };

  const getStatusColor = (status: TestResult['status']) => {
    switch (status) {
      case 'success': return 'text-green-600 bg-green-50 border-green-200';
      case 'error': return 'text-red-600 bg-red-50 border-red-200';
      case 'loading': return 'text-blue-600 bg-blue-50 border-blue-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getStatusIcon = (status: TestResult['status']) => {
    switch (status) {
      case 'success': return '✅';
      case 'error': return '❌';
      case 'loading': return '⏳';
      default: return '❓';
    }
  };

  const successCount = tests.filter(t => t.status === 'success').length;
  const totalTests = tests.length;
  const overallHealth = totalTests > 0 ? (successCount / totalTests) * 100 : 0;

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-sm border border-gray-200">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          🔧 Frontend Diagnostics
        </h2>
        <div className="flex items-center space-x-4">
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            overallHealth >= 80 ? 'bg-green-100 text-green-800' :
            overallHealth >= 60 ? 'bg-yellow-100 text-yellow-800' :
            'bg-red-100 text-red-800'
          }`}>
            {overallHealth.toFixed(0)}% Healthy
          </div>
          <div className="text-sm text-gray-600">
            {successCount}/{totalTests} tests passed
          </div>
          <button
            onClick={runDiagnostics}
            className="px-3 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded text-sm transition-colors"
          >
            🔄 Re-run Tests
          </button>
        </div>
      </div>

      <div className="space-y-3">
        {tests.map((test) => (
          <div
            key={test.test}
            className={`p-4 rounded-lg border ${getStatusColor(test.status)}`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-lg">{getStatusIcon(test.status)}</span>
                <div>
                  <h3 className="font-medium">{test.test}</h3>
                  <p className="text-sm opacity-75">{test.message}</p>
                </div>
              </div>
              {test.data && (
                <div className="text-xs font-mono bg-white bg-opacity-50 px-2 py-1 rounded">
                  {typeof test.data === 'object' ? JSON.stringify(test.data) : String(test.data)}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="font-medium text-blue-900 mb-2">📊 System Status</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-blue-700 font-medium">Frontend:</span>
            <span className="ml-2">{overallHealth >= 80 ? '🟢 Operational' : '🟡 Issues Detected'}</span>
          </div>
          <div>
            <span className="text-blue-700 font-medium">Backend:</span>
            <span className="ml-2">
              {tests.find(t => t.test === 'API Health Check')?.status === 'success' ? '🟢 Online' : '🔴 Offline'}
            </span>
          </div>
        </div>
        <div className="mt-3 text-xs text-blue-600">
          💡 If tests are failing, check: 1) Backend is running on port 8000, 2) Browser console for errors, 3) Network connectivity
        </div>
      </div>
    </div>
  );
};

export default FrontendDiagnostics;
