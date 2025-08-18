import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  ExclamationTriangleIcon,
  ClockIcon,
  CheckCircleIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';
import { useSystemHealth } from '../../hooks/useSystemHealth';

interface ConflictEvent {
  id: string;
  title: string;
  start_time: string;
  end_time: string;
  priority_level?: number;
}

interface DetectedConflict {
  id: string;
  timeSlot: string;
  events: ConflictEvent[];
  severity: 'low' | 'medium' | 'high';
  suggestedResolution: string;
  bertAnalysis?: {
    confidence: number;
    reasoning: string;
  };
}

const ConflictDetectionPanel: React.FC = () => {
  const [conflicts, setConflicts] = useState<DetectedConflict[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { systemHealth } = useSystemHealth();

  useEffect(() => {
    console.log('ConflictDetectionPanel mounted');
    detectConflicts();
  }, []);

  const detectConflicts = async () => {
    try {
      setIsLoading(true);
      console.log('Starting conflict detection...');
      
      // Get all events
      const events = await apiService.getEvents();
      console.log(`Retrieved ${events.length} events`);

      if (events.length < 2) {
        console.log('Not enough events to detect conflicts');
        setConflicts([]);
        return;
      }

      // Check each event for conflicts with other events
      const allDetectedConflicts: DetectedConflict[] = [];
      
      for (let i = 0; i < events.length; i++) {
        const event = events[i];
        
        try {
          const payload = {
            title: event.title,
            start_time: event.start_time,
            end_time: event.end_time,
            description: event.description || '',
            is_all_day: (event as any).is_all_day || (event as any).all_day || false
          };

          console.log(`Checking conflicts for: ${event.title}`);
          const response = await apiService.conflictsCheck(payload);

          if (response?.conflicts && response.conflicts.length > 0) {
            // Transform each backend conflict to frontend format
            for (const conflict of response.conflicts) {
              const detectedConflict: DetectedConflict = {
                id: conflict.conflict_id || `conflict-${Date.now()}-${Math.random()}`,
                timeSlot: event.start_time,
                events: [
                  {
                    id: event.id || 'unknown',
                    title: event.title,
                    start_time: event.start_time,
                    end_time: event.end_time,
                    priority_level: event.priority_level || 3
                  },
                  {
                    id: conflict.affected_event_ids?.[0] || 'unknown-conflict',
                    title: conflict.priority_analysis?.existing_event?.title || 'Conflicting Event',
                    start_time: event.start_time,
                    end_time: event.end_time,
                    priority_level: conflict.priority_analysis?.existing_event?.priority || 3
                  }
                ],
                severity: conflict.severity || 'medium',
                suggestedResolution: conflict.description || 'Reschedule one of the conflicting events',
                bertAnalysis: {
                  confidence: conflict.ai_confidence || 0.9,
                  reasoning: conflict.reasoning?.join(', ') || 'BERT AI detected scheduling conflict'
                }
              };
              
              // Avoid duplicates by checking if similar conflict already exists
              const isDuplicate = allDetectedConflicts.some(existing => 
                existing.timeSlot === detectedConflict.timeSlot &&
                existing.suggestedResolution.includes(conflict.priority_analysis?.existing_event?.title || '')
              );
              
              if (!isDuplicate) {
                allDetectedConflicts.push(detectedConflict);
                console.log(`Added conflict: ${event.title} vs ${conflict.priority_analysis?.existing_event?.title}`);
              }
            }
          }
        } catch (error) {
          console.error(`Error checking conflicts for ${event.title}:`, error);
        }
      }

      console.log(`Total unique conflicts detected: ${allDetectedConflicts.length}`);
      setConflicts(allDetectedConflicts);

    } catch (error) {
      console.error('Error in conflict detection:', error);
      setConflicts([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Helper functions for UI
  const getSeverityColor = (severity: 'low' | 'medium' | 'high') => {
    switch (severity) {
      case 'high': return 'bg-red-50 border-red-200 text-red-800';
      case 'medium': return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'low': return 'bg-blue-50 border-blue-200 text-blue-800';
      default: return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getSeverityIcon = (severity: 'low' | 'medium' | 'high') => {
    switch (severity) {
      case 'high': return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      case 'medium': return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      case 'low': return <CalendarIcon className="h-5 w-5 text-blue-500" />;
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-purple-100 rounded-lg">
            <ExclamationTriangleIcon className="h-6 w-6 text-purple-600" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900">🧠 Smart Conflict Detection</h2>
        </div>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          <span className="ml-3 text-gray-600">Analyzing conflicts with BERT AI...</span>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      key={`conflicts-panel-${conflicts.length}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-purple-100 rounded-lg">
            <ExclamationTriangleIcon className="h-6 w-6 text-purple-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">🧠 Smart Conflict Detection</h2>
            <span className="ml-3 text-xs font-normal text-gray-500">BERT AI Powered</span>
          </div>
        </div>
        
        <button
          onClick={detectConflicts}
          disabled={isLoading}
          className="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          {isLoading ? 'Analyzing...' : 'Refresh Analysis'}
        </button>
      </div>

      {/* Conflicts Display */}
      {conflicts.length === 0 ? (
        <div className="text-center py-12">
          <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Conflicts Detected</h3>
          <p className="text-gray-600">BERT AI analysis shows your schedule is well-organized!</p>
        </div>
      ) : (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Found {conflicts.length} Scheduling Conflicts
          </h3>
          
          {conflicts.map((conflict) => (
            <motion.div
              key={conflict.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className={`border rounded-lg p-4 ${getSeverityColor(conflict.severity)}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  {getSeverityIcon(conflict.severity)}
                  <div>
                    <h4 className="font-medium">
                      Conflict at {new Date(conflict.timeSlot).toLocaleTimeString()}
                    </h4>
                    <p className="text-sm opacity-75 mt-1">{conflict.suggestedResolution}</p>
                  </div>
                </div>
              </div>

              {/* Conflicting Events */}
              <div className="mt-4 space-y-2">
                <h5 className="font-medium text-sm">Conflicting Events ({conflict.events.length}):</h5>
                {conflict.events.map((event, idx) => (
                  <div key={`${event.id}-${idx}`} className="flex items-center justify-between bg-white bg-opacity-50 rounded-lg p-3">
                    <div>
                      <div className="font-medium">{event.title}</div>
                      <div className="text-sm opacity-75">
                        {new Date(event.start_time).toLocaleString()} - {new Date(event.end_time).toLocaleString()}
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-1 bg-white bg-opacity-75 rounded text-xs font-medium">
                        P{event.priority_level || 3}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* BERT Analysis */}
              {conflict.bertAnalysis && (
                <div className="mt-4 p-3 bg-white bg-opacity-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-xs font-medium bg-purple-100 text-purple-800 px-2 py-1 rounded">
                      🤖 BERT AI Analysis
                    </span>
                    <span className="text-xs text-gray-600">
                      {Math.round(conflict.bertAnalysis.confidence * 100)}% confidence
                    </span>
                  </div>
                  <p className="text-sm">{conflict.bertAnalysis.reasoning}</p>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      )}
      
      {/* System Health Indicator */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>BERT AI Status:</span>
          <span className={systemHealth?.bert ? 'text-green-600' : 'text-red-600'}>
            {systemHealth?.bert ? '🟢 Online' : '🔴 Offline'}
          </span>
        </div>
      </div>
    </motion.div>
  );
};

export default ConflictDetectionPanel;
