import React from 'react';
import { motion } from 'framer-motion';
import { 
  ExclamationTriangleIcon, 
  XMarkIcon, 
  ClockIcon,
  CalendarDaysIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';
import type { Event } from '../../../services/apiService';

export interface ConflictInfo {
  type: 'overlap' | 'proximity' | 'travel_time' | 'priority_clash';
  severity: 'low' | 'medium' | 'high';
  conflictingEvents: Event[];
  message: string;
  suggestion?: string;
  confidence?: number;
}

export interface ConflictWarningProps {
  conflicts: ConflictInfo[];
  event: Event;
  onResolve?: (conflictType: string, resolution: 'ignore' | 'reschedule' | 'modify') => void;
  onDismiss?: () => void;
  className?: string;
}

const SEVERITY_STYLES = {
  low: {
    background: 'bg-yellow-50',
    border: 'border-yellow-200',
    icon: 'text-yellow-600',
    button: 'bg-yellow-100 hover:bg-yellow-200 text-yellow-700',
  },
  medium: {
    background: 'bg-orange-50', 
    border: 'border-orange-200',
    icon: 'text-orange-600',
    button: 'bg-orange-100 hover:bg-orange-200 text-orange-700',
  },
  high: {
    background: 'bg-red-50',
    border: 'border-red-200', 
    icon: 'text-red-600',
    button: 'bg-red-100 hover:bg-red-200 text-red-700',
  },
};

const CONFLICT_ICONS = {
  overlap: CalendarDaysIcon,
  proximity: ClockIcon,
  travel_time: ArrowRightIcon,
  priority_clash: ExclamationTriangleIcon,
};

const ConflictWarning: React.FC<ConflictWarningProps> = ({
  conflicts,
  event,
  onResolve,
  onDismiss,
  className = '',
}) => {
  if (!conflicts || conflicts.length === 0) return null;

  // Get the highest severity conflict to determine overall styling
  const maxSeverity = conflicts.reduce((max, conflict) => {
    const severityOrder = { low: 1, medium: 2, high: 3 };
    return severityOrder[conflict.severity] > severityOrder[max] ? conflict.severity : max;
  }, 'low' as 'low' | 'medium' | 'high');

  const styles = SEVERITY_STYLES[maxSeverity];

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    });
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -10, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -10, scale: 0.95 }}
      className={`
        ${styles.background} ${styles.border}
        border rounded-lg p-4 shadow-lg ${className}
      `}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          <ExclamationTriangleIcon className={`h-5 w-5 ${styles.icon}`} />
          <div>
            <h4 className="font-semibold text-gray-900">
              Scheduling Conflict{conflicts.length > 1 ? 's' : ''} Detected
            </h4>
            <p className="text-sm text-gray-600">
              {conflicts.length} conflict{conflicts.length > 1 ? 's' : ''} found for "{event.title}"
            </p>
          </div>
        </div>
        
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="p-1 hover:bg-gray-200 rounded transition-colors"
            aria-label="Dismiss warning"
          >
            <XMarkIcon className="h-4 w-4 text-gray-500" />
          </button>
        )}
      </div>

      {/* Conflict Details */}
      <div className="space-y-3">
        {conflicts.map((conflict, index) => {
          const ConflictIcon = CONFLICT_ICONS[conflict.type];
          
          return (
            <div key={index} className="bg-white rounded-lg p-3 border border-gray-200">
              <div className="flex items-start space-x-3">
                <div className="p-1.5 bg-gray-100 rounded">
                  <ConflictIcon className="h-4 w-4 text-gray-600" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-sm font-medium text-gray-900 capitalize">
                      {conflict.type.replace('_', ' ')}
                    </span>
                    <span className={`
                      px-2 py-0.5 text-xs font-medium rounded-full
                      ${conflict.severity === 'high' ? 'bg-red-100 text-red-800' :
                        conflict.severity === 'medium' ? 'bg-orange-100 text-orange-800' :
                        'bg-yellow-100 text-yellow-800'}
                    `}>
                      {conflict.severity}
                    </span>
                    {conflict.confidence && (
                      <span className="text-xs text-gray-500">
                        {Math.round(conflict.confidence * 100)}% confidence
                      </span>
                    )}
                  </div>
                  
                  <p className="text-sm text-gray-700 mb-2">
                    {conflict.message}
                  </p>
                  
                  {conflict.suggestion && (
                    <p className="text-xs text-gray-600 bg-gray-50 rounded p-2">
                      💡 <strong>Suggestion:</strong> {conflict.suggestion}
                    </p>
                  )}
                  
                  {/* Conflicting Events */}
                  {conflict.conflictingEvents.length > 0 && (
                    <div className="mt-2 space-y-1">
                      <p className="text-xs font-medium text-gray-700">
                        Conflicts with:
                      </p>
                      {conflict.conflictingEvents.map((conflictEvent) => (
                        <div
                          key={conflictEvent.id}
                          className="flex items-center justify-between text-xs bg-gray-50 rounded px-2 py-1"
                        >
                          <div className="flex items-center space-x-2 min-w-0">
                            <div className={`
                              w-2 h-2 rounded-full flex-shrink-0
                              ${conflictEvent.priority_level === 1 ? 'bg-red-500' :
                                conflictEvent.priority_level === 2 ? 'bg-orange-500' :
                                conflictEvent.priority_level === 3 ? 'bg-blue-500' :
                                conflictEvent.priority_level === 4 ? 'bg-green-500' :
                                'bg-gray-500'}
                            `} />
                            <span className="font-medium truncate">
                              {conflictEvent.title}
                            </span>
                          </div>
                          <div className="text-gray-600 flex-shrink-0 ml-2">
                            {formatDate(conflictEvent.start_time)} {formatTime(conflictEvent.start_time)}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Resolution Actions */}
      {onResolve && conflicts.length > 0 && (
        <div className="mt-4 pt-3 border-t border-gray-200">
          <p className="text-sm font-medium text-gray-700 mb-2">
            How would you like to resolve these conflicts?
          </p>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => onResolve('all', 'ignore')}
              className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded transition-colors"
            >
              Ignore Conflicts
            </button>
            <button
              onClick={() => onResolve('all', 'reschedule')}
              className={`px-3 py-1.5 text-sm rounded transition-colors ${styles.button}`}
            >
              Suggest Reschedule
            </button>
            <button
              onClick={() => onResolve('all', 'modify')}
              className="px-3 py-1.5 text-sm bg-blue-100 hover:bg-blue-200 text-blue-700 rounded transition-colors"
            >
              Modify Event
            </button>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default ConflictWarning;
