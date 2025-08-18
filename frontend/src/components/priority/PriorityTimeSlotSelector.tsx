/**
 * Priority-Based Time Slot Selector Component
 * 
 * NEW COMPONENT: Provides intelligent time slot suggestions based on priority levels
 * Integrates with the new Priority API backend without modifying existing components.
 * 
 * SAFETY: This is an ADDITION that supplements existing functionality
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  ClockIcon,
  SparklesIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  CalendarDaysIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';

interface PriorityTimeSlot {
  start_time: string;
  end_time: string;
  confidence: number;
  reasoning: string;
  priority_match_score: number;
  availability_score: number;
  is_prime_time: boolean;
  conflict_risk: number;
}

interface PrioritySchedulingResult {
  success: boolean;
  message: string;
  original_priority: number;
  suggested_slots: PriorityTimeSlot[];
  reasoning: string;
  total_slots_considered: number;
  filter_criteria_used: string[];
  fallback_used: boolean;
  processing_time_ms: number;
}

interface PriorityTimeSlotSelectorProps {
  priority: number;
  duration: number;
  excludeTimes?: Array<{start: string; end: string}>;
  preferredDate?: string;
  userId?: string;
  onSlotSelected?: (slot: PriorityTimeSlot) => void;
  isVisible?: boolean;
}

const PRIORITY_LABELS: Record<number, {name: string; color: string; icon: string}> = {
  1: { name: 'Very Low', color: 'text-gray-500', icon: '🔽' },
  2: { name: 'Low', color: 'text-blue-500', icon: '⚡' },
  3: { name: 'Medium', color: 'text-yellow-500', icon: '🔸' },
  4: { name: 'High', color: 'text-orange-500', icon: '🔥' },
  5: { name: 'Critical', color: 'text-red-500', icon: '🚨' }
};

export const PriorityTimeSlotSelector: React.FC<PriorityTimeSlotSelectorProps> = ({
  priority,
  duration,
  excludeTimes = [],
  preferredDate,
  userId = 'default_user',
  onSlotSelected,
  isVisible = true
}) => {
  const [suggestions, setSuggestions] = useState<PrioritySchedulingResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<PriorityTimeSlot | null>(null);

  const fetchPrioritySuggestions = async () => {
    if (!priority || !duration) return;

    setLoading(true);
    setError(null);

    try {
      const requestBody = {
        priority_level: priority,
        duration_minutes: duration,
        preferred_date: preferredDate || undefined,
        exclude_times: excludeTimes.length > 0 ? excludeTimes : undefined,
        num_suggestions: 5
      };

      console.log('🎯 Requesting priority suggestions:', requestBody);

      const response = await fetch(`${apiService.getBaseUrl()}/api/v1/priority/resolve?user_id=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`Priority API error: ${response.status}`);
      }

      const result: PrioritySchedulingResult = await response.json();
      console.log('✅ Priority suggestions received:', result);

      setSuggestions(result);
    } catch (err) {
      console.error('❌ Priority suggestions failed:', err);
      setError(err instanceof Error ? err.message : 'Failed to get priority suggestions');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isVisible && priority && duration) {
      fetchPrioritySuggestions();
    }
  }, [priority, duration, preferredDate, excludeTimes, isVisible]);

  const handleSlotSelection = (slot: PriorityTimeSlot) => {
    setSelectedSlot(slot);
    onSlotSelected?.(slot);
  };

  const formatTime = (isoString: string): string => {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatTimeRange = (startTime: string, endTime: string): string => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    
    if (start.toDateString() === end.toDateString()) {
      return `${start.toLocaleDateString()} ${start.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - ${end.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`;
    }
    
    return `${formatTime(startTime)} - ${formatTime(endTime)}`;
  };

  const getPriorityBadge = (priorityLevel: number) => {
    const config = PRIORITY_LABELS[priorityLevel] || PRIORITY_LABELS[3];
    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-opacity-10 ${config.color} bg-current`}>
        <span className="mr-1">{config.icon}</span>
        {config.name} Priority
      </span>
    );
  };

  const getConfidenceIndicator = (confidence: number) => {
    if (confidence >= 0.9) return { color: 'text-green-500', icon: '🎯', text: 'Excellent' };
    if (confidence >= 0.7) return { color: 'text-blue-500', icon: '✨', text: 'Good' };
    if (confidence >= 0.5) return { color: 'text-yellow-500', icon: '⭐', text: 'Fair' };
    return { color: 'text-gray-500', icon: '⚪', text: 'Low' };
  };

  if (!isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-lg shadow-lg p-6 border border-gray-200"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <SparklesIcon className="h-6 w-6 text-purple-500" />
          <h3 className="text-lg font-semibold text-gray-900">
            Smart Time Suggestions
          </h3>
        </div>
        {getPriorityBadge(priority)}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
          <span className="ml-3 text-gray-600">Finding optimal time slots...</span>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">
                Unable to get priority suggestions
              </h3>
              <p className="mt-1 text-sm text-red-700">{error}</p>
              <button
                onClick={fetchPrioritySuggestions}
                className="mt-2 text-sm text-red-600 hover:text-red-500 underline"
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {suggestions && !loading && (
        <div className="space-y-4">
          {/* Summary */}
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
            <div className="flex items-start">
              <SparklesIcon className="h-5 w-5 text-blue-400 mt-0.5" />
              <div className="ml-3">
                <p className="text-sm text-blue-800 font-medium">
                  Smart Analysis Complete
                </p>
                <p className="text-sm text-blue-700 mt-1">
                  {suggestions.reasoning}
                </p>
                <div className="mt-2 text-xs text-blue-600">
                  Processed in {Math.round(suggestions.processing_time_ms)}ms • 
                  {suggestions.suggested_slots.length} suggestions found
                </div>
              </div>
            </div>
          </div>

          {/* Time Slot Options */}
          <div className="space-y-3">
            <h4 className="text-sm font-medium text-gray-900 flex items-center">
              <CalendarDaysIcon className="h-4 w-4 mr-2" />
              Recommended Time Slots
            </h4>
            
            {suggestions.suggested_slots.map((slot, index) => {
              const confidence = getConfidenceIndicator(slot.confidence);
              const isSelected = selectedSlot === slot;

              return (
                <motion.div
                  key={index}
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.99 }}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                    isSelected 
                      ? 'border-purple-500 bg-purple-50' 
                      : 'border-gray-200 hover:border-gray-300 bg-gray-50'
                  }`}
                  onClick={() => handleSlotSelection(slot)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <ClockIcon className="h-5 w-5 text-gray-500" />
                        <span className="font-medium text-gray-900">
                          {formatTimeRange(slot.start_time, slot.end_time)}
                        </span>
                        {slot.is_prime_time && (
                          <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full font-medium">
                            Prime Time
                          </span>
                        )}
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-2">
                        {slot.reasoning}
                      </p>

                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span className={`flex items-center ${confidence.color}`}>
                          {confidence.icon} {confidence.text} Match ({Math.round(slot.confidence * 100)}%)
                        </span>
                        <span>
                          Availability: {Math.round(slot.availability_score * 100)}%
                        </span>
                        {slot.conflict_risk > 0 && (
                          <span className="text-orange-500">
                            Risk: {Math.round(slot.conflict_risk * 100)}%
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="ml-4">
                      {isSelected ? (
                        <CheckCircleIcon className="h-6 w-6 text-purple-500" />
                      ) : (
                        <div className="h-6 w-6 border-2 border-gray-300 rounded-full"></div>
                      )}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Fallback Notice */}
          {suggestions.fallback_used && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
              <div className="flex">
                <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400" />
                <div className="ml-3">
                  <p className="text-sm text-yellow-800">
                    Limited suggestions available. Consider adjusting your priority or timing preferences.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
};

export default PriorityTimeSlotSelector;
