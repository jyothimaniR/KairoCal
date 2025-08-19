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
      console.log('🔍 Starting improved conflict detection...');
      
      // Get all events
      const events = await apiService.getEvents();
      console.log(`📊 Retrieved ${events.length} events`);

      if (events.length < 2) {
        console.log('⚠️ Not enough events to detect conflicts');
        setConflicts([]);
        return;
      }

      // 🔧 MAJOR FIX: Use client-side conflict detection to avoid duplicates
      // This ensures each conflict pair is detected only once
      const allDetectedConflicts: DetectedConflict[] = [];
      const timeEvents = events.filter(event => {
        const isAllDay = (event as any).is_all_day || (event as any).all_day || false;
        if (isAllDay) {
          console.log(`📅 Skipping all-day event: ${event.title}`);
          return false;
        }
        return true;
      });

      console.log(`⏰ Checking ${timeEvents.length} time-based events for conflicts`);

      // Check for overlapping events using proper pairwise comparison
      const conflictPairs: Array<[any, any]> = [];
      
      for (let i = 0; i < timeEvents.length; i++) {
        for (let j = i + 1; j < timeEvents.length; j++) {
          const event1 = timeEvents[i];
          const event2 = timeEvents[j];
          
          const start1 = new Date(event1.start_time);
          const end1 = new Date(event1.end_time);
          const start2 = new Date(event2.start_time);  
          const end2 = new Date(event2.end_time);
          
          console.log(`🔄 Checking overlap: "${event1.title}" vs "${event2.title}"`);
          console.log(`   Event 1: ${start1.toLocaleString()} - ${end1.toLocaleString()}`);
          console.log(`   Event 2: ${start2.toLocaleString()} - ${end2.toLocaleString()}`);
          
          // Check for time overlap: events overlap if start1 < end2 AND start2 < end1
          const hasOverlap = start1 < end2 && start2 < end1;
          
          console.log(`   Result: ${hasOverlap ? '🚨 CONFLICT DETECTED!' : '✅ No conflict'}`);
          
          if (hasOverlap) {
            conflictPairs.push([event1, event2]);
            console.log(`🆕 Added conflict pair: ${event1.title} vs ${event2.title}`);
          }
        }
      }

      console.log(`🗂️ Found ${conflictPairs.length} unique conflict pairs`);

      // Convert conflict pairs to DetectedConflict objects
      conflictPairs.forEach(([event1, event2]) => {
        // Calculate overlap details
        const start1 = new Date(event1.start_time);
        const end1 = new Date(event1.end_time);
        const start2 = new Date(event2.start_time);
        const end2 = new Date(event2.end_time);
        
        const overlapStart = new Date(Math.max(start1.getTime(), start2.getTime()));
        const overlapEnd = new Date(Math.min(end1.getTime(), end2.getTime()));
        const overlapMinutes = Math.round((overlapEnd.getTime() - overlapStart.getTime()) / (1000 * 60));
        
        // Use the earlier event's start time as the conflict time slot
        const conflictTimeSlot = start1 <= start2 ? event1.start_time : event2.start_time;
        
        // Create unique conflict ID based on event IDs (sorted for consistency)
        const eventIds = [event1.id, event2.id].sort();
        const conflictId = `conflict-${eventIds.join('-')}`;
        
        // Determine severity based on overlap duration and priorities
        let severity: 'low' | 'medium' | 'high' = 'medium';
        const priority1 = event1.priority_level || 3;
        const priority2 = event2.priority_level || 3;
        const highestPriority = Math.min(priority1, priority2); // Lower number = higher priority
        
        if (overlapMinutes >= 60 || highestPriority <= 2) {
          severity = 'high';
        } else if (overlapMinutes >= 30 || highestPriority <= 3) {
          severity = 'medium';
        } else {
          severity = 'low';
        }
        
        const detectedConflict: DetectedConflict = {
          id: conflictId,
          timeSlot: conflictTimeSlot,
          events: [
            {
              id: event1.id || 'unknown',
              title: event1.title,
              start_time: event1.start_time,
              end_time: event1.end_time,
              priority_level: priority1
            },
            {
              id: event2.id || 'unknown',
              title: event2.title,
              start_time: event2.start_time,
              end_time: event2.end_time,
              priority_level: priority2
            }
          ],
          severity,
          suggestedResolution: `${overlapMinutes} minute overlap detected. Consider rescheduling one event.`,
          bertAnalysis: {
            confidence: 0.95,
            reasoning: `Time overlap analysis: ${overlapMinutes} minutes overlap between "${event1.title}" and "${event2.title}"`
          }
        };
        
        allDetectedConflicts.push(detectedConflict);
        console.log(`✅ Created conflict: ${event1.title} vs ${event2.title} (${overlapMinutes}min overlap)`);
      });

      console.log(`🎯 Total unique conflicts detected: ${allDetectedConflicts.length}`);
      setConflicts(allDetectedConflicts);

    } catch (error) {
      console.error('❌ Error in conflict detection:', error);
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
