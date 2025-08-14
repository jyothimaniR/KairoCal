/**
 * Quick test for priority alert functionality
 * This can be used to test the Accept button functionality
 */
import React, { useState } from 'react';
import { apiService } from '../../services/apiService';

const PriorityAlertTest: React.FC = () => {
  const [testResult, setTestResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const testPriorityUpdate = async () => {
    setIsLoading(true);
    setTestResult('');

    try {
      console.log('🧪 Testing priority update functionality...');
      
      // Get events first
      const events = await apiService.getEvents();
      console.log('📋 Retrieved events:', events.length);
      
      if (events.length === 0) {
        setTestResult('❌ No events found to test with');
        return;
      }

      const testEvent = events[0];
      console.log('🎯 Testing with event:', testEvent.id, testEvent.title);
      
      const originalPriority = testEvent.priority_level || 3;
      const newPriority = Math.max(1, originalPriority - 1); // Increase priority
      
      console.log('🔄 Updating priority from', originalPriority, 'to', newPriority);
      
      const success = await apiService.updateEventPriority(testEvent.id!, newPriority);
      
      if (success) {
        setTestResult(`✅ Success! Updated "${testEvent.title}" priority from ${originalPriority} to ${newPriority}`);
      } else {
        setTestResult(`❌ Failed to update priority for "${testEvent.title}"`);
      }
      
    } catch (error) {
      console.error('Test error:', error);
      setTestResult(`❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 border border-blue-200 rounded-lg bg-blue-50">
      <h3 className="text-lg font-semibold mb-4">🧪 Priority Alert Test</h3>
      <button 
        onClick={testPriorityUpdate}
        disabled={isLoading}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {isLoading ? 'Testing...' : 'Test Priority Update'}
      </button>
      
      {testResult && (
        <div className="mt-4 p-3 rounded bg-white border">
          <pre className="text-sm">{testResult}</pre>
        </div>
      )}
    </div>
  );
};

export default PriorityAlertTest;
