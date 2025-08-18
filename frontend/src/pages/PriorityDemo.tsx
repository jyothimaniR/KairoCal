/**
 * Priority Components Demo Page
 * 
 * NEW PAGE: Demonstrates the new priority-based scheduling components
 * Allows testing and validation without affecting existing functionality.
 * 
 * SAFETY: This is a standalone demo that doesn't modify existing pages
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  SparklesIcon,
  ClockIcon,
  CpuChipIcon,
  CheckBadgeIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { PriorityEditor, PriorityTimeSlotSelector } from '../components/priority';
import { apiService } from '../services/apiService';

interface DemoState {
  selectedPriority: number;
  eventTitle: string;
  eventDescription: string;
  duration: number;
  selectedTimeSlot: any;
  priorityHealth: any;
  testResults: any;
}

const PriorityDemo: React.FC = () => {
  const [state, setState] = useState<DemoState>({
    selectedPriority: 3,
    eventTitle: 'Team Project Review Meeting',
    eventDescription: 'Weekly review of project progress and planning',
    duration: 60,
    selectedTimeSlot: null,
    priorityHealth: null,
    testResults: null
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load priority system health on component mount
  useEffect(() => {
    const loadSystemHealth = async () => {
      try {
        const health = await apiService.getPriorityHealth();
        setState(prev => ({ ...prev, priorityHealth: health }));
      } catch (err) {
        console.error('Failed to load priority health:', err);
        setError('Priority system health check failed');
      }
    };

    loadSystemHealth();
  }, []);

  // Handle priority changes from the editor
  const handlePriorityChange = (priority: number, confidence?: number, method?: string) => {
    console.log('🎯 Priority changed:', { priority, confidence, method });
    setState(prev => ({ 
      ...prev, 
      selectedPriority: priority,
      selectedTimeSlot: null // Reset time slot when priority changes
    }));
  };

  // Handle time slot selection
  const handleTimeSlotSelected = (slot: any) => {
    console.log('⏰ Time slot selected:', slot);
    setState(prev => ({ ...prev, selectedTimeSlot: slot }));
  };

  // Test priority scheduling functionality
  const runPriorityTest = async () => {
    setLoading(true);
    setError(null);

    try {
      const testResults = await apiService.testPriorityScheduling(
        state.selectedPriority,
        state.duration
      );
      setState(prev => ({ ...prev, testResults }));
    } catch (err) {
      console.error('Priority test failed:', err);
      setError(err instanceof Error ? err.message : 'Priority test failed');
    } finally {
      setLoading(false);
    }
  };

  // Demo event examples
  const demoEvents = [
    {
      title: 'CEO Emergency Meeting',
      description: 'Urgent discussion about budget crisis',
      expectedPriority: 5
    },
    {
      title: 'Coffee with Team',
      description: 'Casual team bonding session',
      expectedPriority: 1
    },
    {
      title: 'Client Presentation',
      description: 'Important product demo for potential client',
      expectedPriority: 4
    },
    {
      title: 'Weekly Standup',
      description: 'Regular team progress update',
      expectedPriority: 3
    }
  ];

  const loadDemoEvent = (event: typeof demoEvents[0]) => {
    setState(prev => ({
      ...prev,
      eventTitle: event.title,
      eventDescription: event.description,
      selectedPriority: event.expectedPriority,
      selectedTimeSlot: null
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center space-x-3 mb-4">
            <SparklesIcon className="h-8 w-8 text-purple-500" />
            <h1 className="text-3xl font-bold text-gray-900">
              Priority-Based Smart Scheduling
            </h1>
            <SparklesIcon className="h-8 w-8 text-purple-500" />
          </div>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Demo of the new intelligent scheduling system that uses BERT AI classification 
            to suggest optimal time slots based on event priority levels.
          </p>
        </motion.div>

        {/* System Status */}
        {state.priorityHealth && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg shadow-lg p-6 mb-8"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <CpuChipIcon className="h-6 w-6 text-green-500 mr-2" />
                System Status
              </h2>
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                state.priorityHealth.health.overall_status === 'healthy'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {state.priorityHealth.health.overall_status === 'healthy' ? '✅ Operational' : '⚠️ Degraded'}
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              {Object.entries(state.priorityHealth.health).map(([key, value]) => {
                if (key === 'overall_status') return null;
                const isHealthy = value === 'available' || value === 'operational';
                return (
                  <div key={key} className="text-center">
                    <div className={`text-lg mb-1 ${isHealthy ? 'text-green-500' : 'text-yellow-500'}`}>
                      {isHealthy ? '✅' : '⚠️'}
                    </div>
                    <div className="font-medium text-gray-900 capitalize">
                      {key.replace(/_/g, ' ')}
                    </div>
                    <div className={`text-xs ${isHealthy ? 'text-green-600' : 'text-yellow-600'}`}>
                      {String(value)}
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}

        {/* Demo Controls */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Event Setup */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="space-y-6"
          >
            {/* Demo Events */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Demo Events
              </h3>
              <div className="space-y-2">
                {demoEvents.map((event, index) => (
                  <button
                    key={index}
                    onClick={() => loadDemoEvent(event)}
                    className="w-full text-left p-3 rounded-lg border-2 border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-colors"
                  >
                    <div className="font-medium text-gray-900">{event.title}</div>
                    <div className="text-sm text-gray-600">{event.description}</div>
                    <div className="text-xs text-purple-600 mt-1">
                      Expected Priority: {event.expectedPriority}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Event Details */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Event Details
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Event Title
                  </label>
                  <input
                    type="text"
                    value={state.eventTitle}
                    onChange={(e) => setState(prev => ({ ...prev, eventTitle: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="Enter event title..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description (Optional)
                  </label>
                  <textarea
                    value={state.eventDescription}
                    onChange={(e) => setState(prev => ({ ...prev, eventDescription: e.target.value }))}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="Enter event description..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Duration (minutes)
                  </label>
                  <select
                    value={state.duration}
                    onChange={(e) => setState(prev => ({ ...prev, duration: Number(e.target.value) }))}
                    title="Select event duration"
                    aria-label="Event duration in minutes"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value={30}>30 minutes</option>
                    <option value={60}>1 hour</option>
                    <option value={90}>1.5 hours</option>
                    <option value={120}>2 hours</option>
                    <option value={180}>3 hours</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Test Controls */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                System Test
              </h3>
              <button
                onClick={runPriorityTest}
                disabled={loading}
                className="w-full flex items-center justify-center space-x-2 py-3 px-4 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                ) : (
                  <CheckBadgeIcon className="h-5 w-5" />
                )}
                <span>Test Priority System</span>
              </button>

              {error && (
                <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex">
                    <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
                    <p className="ml-3 text-sm text-red-700">{error}</p>
                  </div>
                </div>
              )}

              {state.testResults && (
                <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <h4 className="font-medium text-green-900 mb-2">Test Results</h4>
                  <div className="text-sm text-green-700 space-y-1">
                    <div>Status: {state.testResults.test_successful ? '✅ Success' : '❌ Failed'}</div>
                    <div>Suggestions: {state.testResults.suggestions_generated}</div>
                    <div>Time Window: {state.testResults.time_window_used}</div>
                  </div>
                </div>
              )}
            </div>
          </motion.div>

          {/* Middle Column: Priority Editor */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-lg shadow-lg p-6"
          >
            <PriorityEditor
              currentPriority={state.selectedPriority}
              eventTitle={state.eventTitle}
              eventDescription={state.eventDescription}
              onPriorityChange={handlePriorityChange}
              showBertSuggestion={true}
              disabled={false}
              compact={false}
            />
          </motion.div>

          {/* Right Column: Time Slot Suggestions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <PriorityTimeSlotSelector
              priority={state.selectedPriority}
              duration={state.duration}
              onSlotSelected={handleTimeSlotSelected}
              isVisible={true}
              userId="demo_user"
            />

            {/* Selected Time Slot */}
            {state.selectedTimeSlot && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="mt-6 bg-purple-50 border-2 border-purple-200 rounded-lg p-4"
              >
                <div className="flex items-center space-x-2 mb-3">
                  <CheckBadgeIcon className="h-5 w-5 text-purple-500" />
                  <h4 className="font-medium text-purple-900">Selected Time Slot</h4>
                </div>
                <div className="text-sm text-purple-800 space-y-1">
                  <div className="flex items-center space-x-2">
                    <ClockIcon className="h-4 w-4" />
                    <span>
                      {new Date(state.selectedTimeSlot.start_time).toLocaleString()} - 
                      {new Date(state.selectedTimeSlot.end_time).toLocaleTimeString()}
                    </span>
                  </div>
                  <div>Confidence: {Math.round(state.selectedTimeSlot.confidence * 100)}%</div>
                  <div>Prime Time: {state.selectedTimeSlot.is_prime_time ? 'Yes' : 'No'}</div>
                  <div>Risk Level: {Math.round(state.selectedTimeSlot.conflict_risk * 100)}%</div>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center text-gray-500 text-sm"
        >
          <p>
            🚀 Phase 2 Implementation: Frontend Priority Interface Components
          </p>
          <p className="mt-1">
            This demo showcases the new priority-based scheduling system integrated with BERT AI classification.
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default PriorityDemo;
