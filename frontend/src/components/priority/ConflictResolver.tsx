import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';

interface ConflictEvent {
  conflict_id: string;
  conflict_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  affected_event_ids: string[];
  description: string;
  priority_analysis: {
    proposed_event: {
      priority: number;
      confidence: number;
      method: string;
    };
    existing_event: {
      priority: number;
      title: string;
      duration_minutes: number;
    };
  };
  reasoning: string[];
  ai_confidence: number;
}

interface ConflictResolverProps {
  eventData: {
    title: string;
    start_time: string;
    end_time: string;
    description?: string;
  };
  onResolved: () => void;
  onCancel: () => void;
}

const ConflictResolver: React.FC<ConflictResolverProps> = ({
  eventData,
  onResolved,
  onCancel
}) => {
  const [conflicts, setConflicts] = useState<ConflictEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [resolving, setResolving] = useState(false);
  const [selectedResolution, setSelectedResolution] = useState<string>('');

  useEffect(() => {
    checkForConflicts();
  }, [eventData]);

  const checkForConflicts = async () => {
    try {
      setLoading(true);
      const response = await apiService.checkConflicts('frontend-test-user', {
        title: eventData.title,
        start_time: eventData.start_time,
        end_time: eventData.end_time,
        description: eventData.description || ''
      });
      
      setConflicts(response.conflicts || []);
    } catch (error) {
      console.error('Error checking conflicts:', error);
      setConflicts([]);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityLabel = (priority: number) => {
    const labels = ['', 'Very Low', 'Low', 'Medium', 'High', 'Critical'];
    return labels[priority] || 'Unknown';
  };

  const getResolutionSuggestions = (conflict: ConflictEvent) => {
    const suggestions = [];
    const proposedPriority = conflict.priority_analysis.proposed_event.priority;
    const existingPriority = conflict.priority_analysis.existing_event.priority;
    
    if (proposedPriority > existingPriority) {
      suggestions.push({
        id: `reschedule_existing_${conflict.conflict_id}`,
        label: `Reschedule "${conflict.priority_analysis.existing_event.title}" (Lower Priority)`,
        action: 'reschedule_existing',
        reasoning: 'New event has higher priority'
      });
    } else if (existingPriority > proposedPriority) {
      suggestions.push({
        id: `reschedule_new_${conflict.conflict_id}`,
        label: 'Reschedule this new event (Lower Priority)',
        action: 'reschedule_new',
        reasoning: 'Existing event has higher priority'
      });
    }
    
    // Always offer both options
    suggestions.push({
      id: `shorten_new_${conflict.conflict_id}`,
      label: 'Shorten this new event',
      action: 'shorten_new',
      reasoning: 'Reduce overlap by shortening duration'
    });

    suggestions.push({
      id: `find_alternative_${conflict.conflict_id}`,
      label: 'Find alternative time slot',
      action: 'find_alternative',
      reasoning: 'AI will suggest optimal time slots'
    });

    return suggestions;
  };

  const handleResolveConflict = async () => {
    if (!selectedResolution) return;
    
    try {
      setResolving(true);
      
      // Parse the selected resolution
      const [action] = selectedResolution.split('_').slice(-2);
      
      if (action === 'alternative') {
        // Request priority-based time slot suggestions
        const suggestions = await apiService.getPriorityTimeSlots({
          priority_level: conflicts[0]?.priority_analysis.proposed_event.priority || 3,
          duration_minutes: calculateDuration(eventData.start_time, eventData.end_time),
          user_id: 'frontend-test-user',
          preferred_date: new Date(eventData.start_time).toISOString().split('T')[0]
        });
        
        if (suggestions.suggested_slots && suggestions.suggested_slots.length > 0) {
          const bestSlot = suggestions.suggested_slots[0];
          // Update the event with the new time slot
          console.log('Best alternative slot:', bestSlot);
          // Here you would update the event with the new time
        }
      }
      
      // Call the resolution callback
      onResolved();
      
    } catch (error) {
      console.error('Error resolving conflict:', error);
    } finally {
      setResolving(false);
    }
  };

  const calculateDuration = (startTime: string, endTime: string) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    return Math.round((end.getTime() - start.getTime()) / (1000 * 60));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-3">Analyzing potential conflicts...</span>
      </div>
    );
  }

  if (conflicts.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="p-6 bg-green-50 border border-green-200 rounded-lg"
      >
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-8 w-8 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-lg font-medium text-green-800">No Conflicts Detected</h3>
            <p className="text-sm text-green-600">This event can be scheduled without conflicts.</p>
          </div>
        </div>
        <div className="mt-4">
          <button
            onClick={onResolved}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Schedule Event
          </button>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="mb-6">
        <div className="flex items-center mb-2">
          <ExclamationTriangleIcon className="h-8 w-8 text-red-500 mr-3" />
          <h2 className="text-2xl font-bold text-gray-900">Scheduling Conflicts Detected</h2>
        </div>
        <p className="text-gray-600">
          AI has detected {conflicts.length} potential conflicts with your proposed event "{eventData.title}".
        </p>
      </div>

      <div className="space-y-6">
        {conflicts.map((conflict, index) => (
          <motion.div
            key={conflict.conflict_id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="border border-gray-200 rounded-lg overflow-hidden"
          >
            {/* Conflict Header */}
            <div className={`${getSeverityColor(conflict.severity)} p-4 text-white`}>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold capitalize">{conflict.severity} Priority Conflict</h3>
                  <p className="text-sm opacity-90">{conflict.description}</p>
                </div>
                <div className="text-right">
                  <div className="text-sm opacity-90">AI Confidence</div>
                  <div className="text-lg font-bold">{Math.round(conflict.ai_confidence * 100)}%</div>
                </div>
              </div>
            </div>

            {/* Conflict Details */}
            <div className="p-4 bg-gray-50">
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">New Event</h4>
                  <div className="bg-white p-3 rounded border">
                    <div className="font-medium">{eventData.title}</div>
                    <div className="text-sm text-gray-600">
                      Priority: {getPriorityLabel(conflict.priority_analysis.proposed_event.priority)} 
                      ({Math.round(conflict.priority_analysis.proposed_event.confidence * 100)}% confidence)
                    </div>
                    <div className="text-sm text-gray-500">
                      Method: {conflict.priority_analysis.proposed_event.method}
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Existing Event</h4>
                  <div className="bg-white p-3 rounded border">
                    <div className="font-medium">{conflict.priority_analysis.existing_event.title}</div>
                    <div className="text-sm text-gray-600">
                      Priority: {getPriorityLabel(conflict.priority_analysis.existing_event.priority)}
                    </div>
                    <div className="text-sm text-gray-500">
                      Duration: {conflict.priority_analysis.existing_event.duration_minutes} minutes
                    </div>
                  </div>
                </div>
              </div>

              {/* AI Reasoning */}
              <div className="mb-4">
                <h5 className="font-medium text-gray-900 mb-2">AI Analysis</h5>
                <ul className="list-disc list-inside text-sm text-gray-600">
                  {conflict.reasoning.map((reason, idx) => (
                    <li key={idx}>{reason}</li>
                  ))}
                </ul>
              </div>

              {/* Resolution Options */}
              <div>
                <h5 className="font-medium text-gray-900 mb-3">Recommended Resolutions</h5>
                <div className="space-y-2">
                  {getResolutionSuggestions(conflict).map((suggestion) => (
                    <label
                      key={suggestion.id}
                      className="flex items-start p-3 border border-gray-200 rounded cursor-pointer hover:bg-gray-50"
                    >
                      <input
                        type="radio"
                        name="resolution"
                        value={suggestion.id}
                        checked={selectedResolution === suggestion.id}
                        onChange={(e) => setSelectedResolution(e.target.value)}
                        className="mt-1 mr-3"
                      />
                      <div>
                        <div className="font-medium">{suggestion.label}</div>
                        <div className="text-sm text-gray-600">{suggestion.reasoning}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex justify-end space-x-4">
        <button
          onClick={onCancel}
          className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          onClick={handleResolveConflict}
          disabled={!selectedResolution || resolving}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {resolving ? (
            <>
              <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
              Resolving...
            </>
          ) : (
            'Apply Resolution'
          )}
        </button>
      </div>
    </div>
  );
};

export default ConflictResolver;
