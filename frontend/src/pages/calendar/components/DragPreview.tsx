import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ExclamationTriangleIcon, ClockIcon } from '@heroicons/react/24/outline';
import type { Event } from '../../../services/apiService';
import { getPriorityInfo } from '../../../utils/priorityUtils';

interface DragPreviewProps {
  isDragging: boolean;
  draggedEvent: Event | null;
  previewTime: Date | null;
  conflictingEvents: Event[];
  position: { x: number; y: number };
}

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });
};

const DragPreview: React.FC<DragPreviewProps> = ({
  isDragging,
  draggedEvent,
  previewTime,
  conflictingEvents,
  position,
}) => {
  if (!isDragging || !draggedEvent || !previewTime) return null;

  const priority = getPriorityInfo(draggedEvent.priority_level);
  const eventDuration = new Date(draggedEvent.end_time).getTime() - 
                       new Date(draggedEvent.start_time).getTime();
  const previewEndTime = new Date(previewTime.getTime() + eventDuration);
  
  const hasConflicts = conflictingEvents.length > 0;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.8 }}
        className="fixed pointer-events-none z-50"
        style={{
          left: position.x + 10,
          top: position.y - 20,
        }}
      >
        {/* Main preview card */}
        <div className={`
          bg-white rounded-lg shadow-2xl border-2 p-4 min-w-64 max-w-80
          ${hasConflicts ? 'border-red-400 bg-red-50' : `border-${priority.color}-400`}
        `}>
          {/* Header */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h4 className={`font-semibold text-sm ${priority.textColor}`}>
                {draggedEvent.title}
              </h4>
              <div className="flex items-center space-x-2 mt-1">
                <span className={`
                  px-2 py-1 text-xs rounded-full
                  bg-${priority.color}-100 text-${priority.color}-700
                `}>
                  {priority.label}
                </span>
              </div>
            </div>
            
            {hasConflicts && (
              <ExclamationTriangleIcon className="h-5 w-5 text-red-500 flex-shrink-0" />
            )}
          </div>

          {/* New time display */}
          <div className="flex items-center space-x-2 text-sm mb-2">
            <ClockIcon className="h-4 w-4 text-gray-400" />
            <span className="text-gray-700">
              {formatTime(previewTime)} - {formatTime(previewEndTime)}
            </span>
          </div>

          {/* Conflict warning */}
          {hasConflicts && (
            <div className="bg-red-100 border border-red-300 rounded p-2 text-xs">
              <div className="flex items-center space-x-1 text-red-700 mb-1">
                <ExclamationTriangleIcon className="h-3 w-3" />
                <span className="font-medium">Scheduling Conflict</span>
              </div>
              <p className="text-red-600">
                Overlaps with {conflictingEvents.length} event{conflictingEvents.length !== 1 ? 's' : ''}:
              </p>
              <div className="mt-1 space-y-1">
                {conflictingEvents.slice(0, 2).map(event => (
                  <div key={event.id} className="text-red-600 truncate">
                    • {event.title}
                  </div>
                ))}
                {conflictingEvents.length > 2 && (
                  <div className="text-red-500 text-xs">
                    ...and {conflictingEvents.length - 2} more
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Action hint */}
          <div className="mt-3 pt-2 border-t border-gray-200 text-xs text-gray-500">
            {hasConflicts ? 'Release to move with conflicts' : 'Release to move here'}
          </div>
        </div>

        {/* Drop indicator line */}
        <motion.div
          className={`
            absolute -left-2 top-1/2 w-1 h-8 rounded-full transform -translate-y-1/2
            ${hasConflicts ? 'bg-red-500' : 'bg-blue-500'}
          `}
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      </motion.div>
    </AnimatePresence>
  );
};

export default DragPreview;
