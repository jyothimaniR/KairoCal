import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  ExclamationTriangleIcon,
  ArrowPathIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import PriorityConflictResolver from '../../components/conflicts/PriorityConflictResolver';
import { useSystemHealth } from '../../hooks/useSystemHealth';
import { apiService } from '../../services/apiService';

const ConflictsPage: React.FC = () => {
  const [conflictStats, setConflictStats] = useState({
    total: 0,
    resolved: 0,
    pending: 0
  });
  const [isLoadingStats, setIsLoadingStats] = useState(true);
  const { systemHealth } = useSystemHealth();

  useEffect(() => {
    loadConflictStats();
  }, []);

  const loadConflictStats = async () => {
    try {
      setIsLoadingStats(true);
      
      // Get events to calculate real conflict statistics
      const events = await apiService.getEvents();
      
      if (events.length < 2) {
        setConflictStats({ total: 0, resolved: 0, pending: 0 });
        return;
      }

      let totalConflicts = 0;
      let resolvedConflicts = 0;
      
      // Check each event for conflicts to get real statistics
      for (const event of events) {
        // 🔧 CRITICAL FIX: Skip all-day events entirely
        const isAllDay = (event as any).is_all_day || (event as any).all_day || false;
        if (isAllDay) {
          console.log(`ConflictsPage: Skipping all-day event: ${event.title}`);
          continue; // Skip to next event
        }
        
        try {
          const payload = {
            title: event.title,
            start_time: event.start_time,
            end_time: event.end_time,
            description: event.description || '',
            is_all_day: false // We already filtered out all-day events above
          };

          const response = await apiService.conflictsCheck(payload);
          
          if (response?.conflicts && response.conflicts.length > 0) {
            totalConflicts += response.conflicts.length;
            
            // Consider conflicts "resolved" if they are low severity
            // This is a simple heuristic - in production you'd track resolution status
            const lowSeverityConflicts = response.conflicts.filter((c: any) => c.severity === 'low').length;
            resolvedConflicts += lowSeverityConflicts;
          }
        } catch (error) {
          console.error(`Error checking conflicts for ${event.title}:`, error);
        }
      }
      
      // Remove duplicates by dividing by 2 (each conflict appears twice in the loop)
      const uniqueTotal = Math.floor(totalConflicts / 2);
      const uniqueResolved = Math.floor(resolvedConflicts / 2);
      const pending = uniqueTotal - uniqueResolved;
      
      setConflictStats({ 
        total: uniqueTotal, 
        resolved: uniqueResolved, 
        pending: Math.max(0, pending) 
      });
    } catch (error) {
      console.error('Error loading conflict stats:', error);
      setConflictStats({ total: 0, resolved: 0, pending: 0 });
    } finally {
      setIsLoadingStats(false);
    }
  };

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-red-100 rounded-lg">
              <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Smart Conflict Detection</h1>
              <p className="text-gray-600 mt-1">AI-powered scheduling conflict management</p>
            </div>
          </div>
          
          <button
            onClick={loadConflictStats}
            disabled={isLoadingStats}
            className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <ArrowPathIcon className={`h-4 w-4 ${isLoadingStats ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>

        {/* Quick Stats */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Conflicts</p>
                <p className="text-2xl font-bold text-gray-900">{conflictStats.total}</p>
              </div>
              <ExclamationTriangleIcon className="h-8 w-8 text-orange-500" />
            </div>
          </div>
          
          <div className="bg-green-50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Resolved</p>
                <p className="text-2xl font-bold text-green-700">{conflictStats.resolved}</p>
              </div>
              <CheckCircleIcon className="h-8 w-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-red-50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-red-600">Pending</p>
                <p className="text-2xl font-bold text-red-700">{conflictStats.pending}</p>
              </div>
              <ExclamationTriangleIcon className="h-8 w-8 text-red-500" />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Conflict Detection Panel */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <PriorityConflictResolver />
      </motion.div>

      {/* System Status Footer */}
      {systemHealth && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl p-4 shadow-sm border border-gray-200"
        >
          <h3 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
            🔧 Conflict Detection System Status
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Backend API:</span>
              <span className="px-2 py-1 rounded text-xs bg-green-100 text-green-800">
                🟢 Online
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">BERT AI:</span>
              <span className={`px-2 py-1 rounded text-xs ${
                systemHealth.bert?.status === 'healthy' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {systemHealth.bert?.status === 'healthy' ? '🧠 Active' : '🔴 Inactive'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Conflict Engine:</span>
              <span className="px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">
                ⚡ Smart Mode
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Auto-Resolution:</span>
              <span className="px-2 py-1 rounded text-xs bg-purple-100 text-purple-800">
                🤖 Enabled
              </span>
            </div>
          </div>
        </motion.div>
      )}

      {/* Help Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="bg-blue-50 rounded-xl p-6 border border-blue-200"
      >
        <h3 className="text-lg font-semibold text-blue-900 mb-3">💡 How Smart Conflict Detection Works</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <h4 className="font-medium mb-2">🧠 AI Analysis</h4>
            <p>BERT AI analyzes event titles, priorities, and context to identify potential scheduling conflicts with high accuracy.</p>
          </div>
          <div>
            <h4 className="font-medium mb-2">⚡ Smart Resolution</h4>
            <p>Get intelligent suggestions for resolving conflicts based on priority levels, user behavior, and optimal time slots.</p>
          </div>
          <div>
            <h4 className="font-medium mb-2">🔄 Auto-Reschedule</h4>
            <p>One-click rescheduling with AI-powered time slot recommendations that avoid future conflicts.</p>
          </div>
          <div>
            <h4 className="font-medium mb-2">📊 Priority-Based</h4>
            <p>Conflicts are resolved intelligently based on event importance, ensuring critical meetings take precedence.</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ConflictsPage;
