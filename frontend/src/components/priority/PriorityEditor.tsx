/**
 * Priority Level Editor Component
 * 
 * NEW COMPONENT: Allows users to edit event priority levels with visual indicators
 * and integrates with BERT classification for smart suggestions.
 * 
 * SAFETY: This is an ADDITION that supplements existing functionality
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  SparklesIcon,
  ChartBarIcon,
  LightBulbIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';

interface PriorityEditorProps {
  currentPriority?: number;
  eventTitle?: string;
  eventDescription?: string;
  onPriorityChange?: (priority: number, confidence?: number, method?: string) => void;
  showBertSuggestion?: boolean;
  disabled?: boolean;
  compact?: boolean;
}

interface BertClassificationResult {
  priority: number;
  priority_label: string;
  confidence: number;
  classification_method: string;
  event_title: string;
  recommendation: string;
  success: boolean;
}

const PRIORITY_LEVELS = [
  {
    level: 1,
    name: 'Very Low',
    description: 'Optional events, coffee breaks, personal time',
    icon: '🔽',
    color: 'text-gray-500',
    bgColor: 'bg-gray-100',
    borderColor: 'border-gray-300',
    timeWindow: '7 AM - 9 PM (Flexible)'
  },
  {
    level: 2,
    name: 'Low',
    description: 'Casual meetings, routine tasks, social events',
    icon: '⚡',
    color: 'text-blue-500',
    bgColor: 'bg-blue-100',
    borderColor: 'border-blue-300',
    timeWindow: '8 AM - 6 PM (Extended)'
  },
  {
    level: 3,
    name: 'Medium',
    description: 'Regular meetings, standard work, appointments',
    icon: '🔸',
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-100',
    borderColor: 'border-yellow-300',
    timeWindow: '8 AM - 6 PM (Extended)'
  },
  {
    level: 4,
    name: 'High',
    description: 'Important presentations, client meetings, deadlines',
    icon: '🔥',
    color: 'text-orange-500',
    bgColor: 'bg-orange-100',
    borderColor: 'border-orange-300',
    timeWindow: '9 AM - 5 PM (Prime)'
  },
  {
    level: 5,
    name: 'Critical',
    description: 'Urgent CEO meetings, emergencies, crucial deadlines',
    icon: '🚨',
    color: 'text-red-500',
    bgColor: 'bg-red-100',
    borderColor: 'border-red-300',
    timeWindow: '9 AM - 5 PM (Prime)'
  }
];

export const PriorityEditor: React.FC<PriorityEditorProps> = ({
  currentPriority = 3,
  eventTitle = '',
  eventDescription = '',
  onPriorityChange,
  showBertSuggestion = true,
  disabled = false,
  compact = false
}) => {
  const [selectedPriority, setSelectedPriority] = useState(currentPriority);
  const [bertSuggestion, setBertSuggestion] = useState<BertClassificationResult | null>(null);
  const [bertLoading, setBertLoading] = useState(false);
  const [bertError, setBertError] = useState<string | null>(null);
  const [showBertDetails, setShowBertDetails] = useState(false);

  // Get BERT priority suggestion when title or description changes
  const fetchBertSuggestion = async () => {
    if (!showBertSuggestion || !eventTitle.trim()) return;

    setBertLoading(true);
    setBertError(null);

    try {
      const requestBody = {
        text: `${eventTitle} ${eventDescription || ''}`.trim(),
        context: 'academic' // Could be dynamic based on user context
      };

      console.log('🧠 Requesting BERT classification:', requestBody);

      const response = await fetch(`${apiService.getBaseUrl()}/api/v1/nlp/classify-priority`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`BERT API error: ${response.status}`);
      }

      const result: BertClassificationResult = await response.json();
      console.log('✅ BERT classification received:', result);

      setBertSuggestion(result);
    } catch (err) {
      console.error('❌ BERT classification failed:', err);
      setBertError(err instanceof Error ? err.message : 'BERT classification failed');
    } finally {
      setBertLoading(false);
    }
  };

  useEffect(() => {
    if (showBertSuggestion && eventTitle.trim()) {
      const timeoutId = setTimeout(() => {
        fetchBertSuggestion();
      }, 500); // Debounce API calls

      return () => clearTimeout(timeoutId);
    }
  }, [eventTitle, eventDescription, showBertSuggestion]);

  const handlePrioritySelect = (priority: number) => {
    if (disabled) return;

    setSelectedPriority(priority);
    onPriorityChange?.(priority, bertSuggestion?.confidence, 'manual');
  };

  const acceptBertSuggestion = () => {
    if (!bertSuggestion) return;

    setSelectedPriority(bertSuggestion.priority);
    onPriorityChange?.(
      bertSuggestion.priority, 
      bertSuggestion.confidence, 
      bertSuggestion.classification_method
    );
  };

  const getPriorityConfig = (level: number) => {
    return PRIORITY_LEVELS.find(p => p.level === level) || PRIORITY_LEVELS[2];
  };

  if (compact) {
    const currentConfig = getPriorityConfig(selectedPriority);
    
    return (
      <div className="flex items-center space-x-2">
        <span className={`text-lg ${currentConfig.color}`}>
          {currentConfig.icon}
        </span>
        <select
          value={selectedPriority}
          onChange={(e) => handlePrioritySelect(Number(e.target.value))}
          disabled={disabled}
          title="Select event priority level"
          aria-label="Event priority level"
          className={`text-sm border rounded px-2 py-1 ${currentConfig.borderColor} ${currentConfig.bgColor} ${currentConfig.color}`}
        >
          {PRIORITY_LEVELS.map((priority) => (
            <option key={priority.level} value={priority.level}>
              {priority.name} ({priority.level})
            </option>
          ))}
        </select>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <ChartBarIcon className="h-5 w-5 text-purple-500" />
          <h4 className="text-lg font-medium text-gray-900">Event Priority</h4>
        </div>
        {showBertSuggestion && bertSuggestion && (
          <button
            onClick={() => setShowBertDetails(!showBertDetails)}
            className="text-sm text-purple-600 hover:text-purple-500"
          >
            AI Analysis {showBertDetails ? '▲' : '▼'}
          </button>
        )}
      </div>

      {/* BERT Suggestion */}
      {showBertSuggestion && (
        <div className="space-y-3">
          {bertLoading && (
            <div className="flex items-center justify-center py-4 bg-gray-50 rounded-lg">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-500"></div>
              <span className="ml-2 text-sm text-gray-600">AI analyzing priority...</span>
            </div>
          )}

          {bertError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3">
              <div className="flex">
                <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
                <div className="ml-3">
                  <p className="text-sm text-red-800">AI analysis failed: {bertError}</p>
                  <button
                    onClick={fetchBertSuggestion}
                    className="mt-1 text-sm text-red-600 hover:text-red-500 underline"
                  >
                    Retry
                  </button>
                </div>
              </div>
            </div>
          )}

          {bertSuggestion && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-4"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <SparklesIcon className="h-5 w-5 text-purple-500 mt-0.5" />
                  <div>
                    <h5 className="font-medium text-gray-900 mb-1">
                      AI Suggests: {getPriorityConfig(bertSuggestion.priority).name} Priority
                    </h5>
                    <p className="text-sm text-gray-600 mb-2">
                      {bertSuggestion.recommendation}
                    </p>
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <span>Confidence: {Math.round(bertSuggestion.confidence * 100)}%</span>
                      <span>Method: {bertSuggestion.classification_method}</span>
                    </div>
                  </div>
                </div>
                
                {bertSuggestion.priority !== selectedPriority && (
                  <button
                    onClick={acceptBertSuggestion}
                    className="flex items-center space-x-1 px-3 py-1 bg-purple-500 text-white text-sm rounded-md hover:bg-purple-600 transition-colors"
                  >
                    <CheckCircleIcon className="h-4 w-4" />
                    <span>Accept</span>
                  </button>
                )}
              </div>

              {/* BERT Details */}
              {showBertDetails && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="mt-3 pt-3 border-t border-purple-200"
                >
                  <div className="text-xs text-gray-600 space-y-1">
                    <div>Event analyzed: "{bertSuggestion.event_title}"</div>
                    <div>Classification method: {bertSuggestion.classification_method}</div>
                    <div>Processing successful: {bertSuggestion.success ? 'Yes' : 'No'}</div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}
        </div>
      )}

      {/* Priority Level Options */}
      <div className="space-y-2">
        {PRIORITY_LEVELS.map((priority) => {
          const isSelected = selectedPriority === priority.level;
          const isBertSuggested = bertSuggestion?.priority === priority.level;

          return (
            <motion.div
              key={priority.level}
              whileHover={{ scale: disabled ? 1 : 1.01 }}
              whileTap={{ scale: disabled ? 1 : 0.99 }}
              className={`p-3 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                disabled 
                  ? 'opacity-50 cursor-not-allowed' 
                  : isSelected
                    ? `${priority.borderColor} ${priority.bgColor}` 
                    : 'border-gray-200 hover:border-gray-300 bg-white'
              }`}
              onClick={() => handlePrioritySelect(priority.level)}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <span className={`text-xl ${priority.color}`}>
                    {priority.icon}
                  </span>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h5 className={`font-medium ${priority.color}`}>
                        {priority.name} ({priority.level})
                      </h5>
                      {isBertSuggested && (
                        <span className="px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full">
                          AI Suggested
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-2">
                      {priority.description}
                    </p>
                    <p className="text-xs text-gray-500">
                      Scheduling window: {priority.timeWindow}
                    </p>
                  </div>
                </div>

                <div className="ml-4">
                  {isSelected ? (
                    <CheckCircleIcon className={`h-6 w-6 ${priority.color}`} />
                  ) : (
                    <div className="h-6 w-6 border-2 border-gray-300 rounded-full"></div>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Help Text */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
        <div className="flex">
          <LightBulbIcon className="h-5 w-5 text-blue-400" />
          <div className="ml-3">
            <h6 className="text-sm font-medium text-blue-900">Priority Guide</h6>
            <p className="text-sm text-blue-700 mt-1">
              Higher priority events are scheduled during prime business hours for maximum effectiveness.
              AI analysis considers your event title and description to suggest the optimal priority level.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default PriorityEditor;
