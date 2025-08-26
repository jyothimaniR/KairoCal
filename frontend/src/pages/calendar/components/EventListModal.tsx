import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { XMarkIcon, ClockIcon, MapPinIcon } from '@heroicons/react/24/outline';
import type { Event } from '../../../services/apiService';
import { getPriorityInfo } from '../../../utils/priorityUtils';

export interface EventListModalProps {
  isOpen: boolean;
  onClose: () => void;
  date: Date;
  events: Event[];
  onEventClick?: (event: Event) => void;
  onCreateEvent?: (date: Date) => void;
}

const formatTime = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });
  } catch {
    return '';
  }
};

const formatDateRange = (startTime: string, endTime: string): string => {
  try {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const startStr = start.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });
    const endStr = end.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });
    return `${startStr} - ${endStr}`;
  } catch {
    return '';
  }
};

const EventListModal: React.FC<EventListModalProps> = ({
  isOpen,
  onClose,
  date,
  events,
  onEventClick,
  onCreateEvent
}) => {
  const dayName = date.toLocaleDateString(undefined, { weekday: 'long' });
  const dateStr = date.toLocaleDateString(undefined, { 
    month: 'long', 
    day: 'numeric',
    year: 'numeric'
  });

  const sortedEvents = [...events].sort((a, b) => {
    // Sort by start time first
    const timeCompare = new Date(a.start_time).getTime() - new Date(b.start_time).getTime();
    if (timeCompare !== 0) return timeCompare;
    
    // Then by priority (higher number = higher priority, so reverse sort)
    const aPriority = a.priority_level || 3;
    const bPriority = b.priority_level || 3;
    return bPriority - aPriority;
  });

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black bg-opacity-50 z-40"
          />
          
          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", duration: 0.3 }}
            className="fixed top-[20%] left-1/2 transform -translate-x-1/2 z-50 w-full max-w-md mx-4"
          >
            <div className="bg-white rounded-2xl shadow-2xl max-h-[70vh] flex flex-col">
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-200">
                <div>
                  <h2 className="text-xl font-bold text-gray-900">{dayName}</h2>
                  <p className="text-sm text-gray-600">{dateStr}</p>
                </div>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                  aria-label="Close modal"
                >
                  <XMarkIcon className="h-5 w-5 text-gray-500" />
                </button>
              </div>

              {/* Events List */}
              <div className="flex-1 overflow-y-auto">
                {sortedEvents.length === 0 ? (
                  <div className="p-6 text-center text-gray-500">
                    <div className="text-4xl mb-2">📅</div>
                    <p className="text-sm">No events scheduled for this day</p>
                  </div>
                ) : (
                  <div className="p-3 space-y-2">
                    {sortedEvents.map((event, index) => {
                      const priority = getPriorityInfo(event.priority_level);
                      const isAllDay = event.all_day || event.is_all_day;
                      
                      return (
                        <motion.div
                          key={`${event.id}-${index}`}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                          onClick={() => onEventClick?.(event)}
                          className={`
                            group p-3 rounded-lg cursor-pointer border-l-4
                            ${priority.bgColor} border-${priority.color}-400
                            hover:shadow-md hover:scale-[1.02] transition-all duration-200
                          `}
                        >
                          {/* Event Title and Priority */}
                          <div className="flex items-start justify-between mb-2">
                            <h3 className={`font-semibold text-sm ${priority.textColor} group-hover:text-gray-900`}>
                              {event.title}
                            </h3>
                            <span className={`text-xs px-2 py-1 rounded-full ${priority.bgColor} ${priority.textColor} opacity-75 ml-2 flex-shrink-0`}>
                              {priority.label}
                            </span>
                          </div>

                          {/* Event Time */}
                          {!isAllDay && (
                            <div className="flex items-center space-x-1 mb-1 text-xs text-gray-600">
                              <ClockIcon className="h-3 w-3" />
                              <span>
                                {event.end_time 
                                  ? formatDateRange(event.start_time, event.end_time)
                                  : formatTime(event.start_time)
                                }
                              </span>
                            </div>
                          )}

                          {isAllDay && (
                            <div className="mb-1">
                              <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                                All Day
                              </span>
                            </div>
                          )}

                          {/* Event Location - Only show if location exists and is not time data */}
                          {event.location && 
                           !event.location.match(/^\d{1,2}:\d{2}\s*(AM|PM|A\.M\.|P\.M\.)?$/i) && 
                           !event.location.match(/^\d{1,2}:\d{2}$/) && 
                           event.location.trim().length > 0 && (
                            <div className="flex items-center space-x-1 mb-1 text-xs text-gray-600">
                              <MapPinIcon className="h-3 w-3" />
                              <span className="truncate">{event.location}</span>
                            </div>
                          )}

                          {/* Event Description - Only if exists, not voice-created text, and not too long */}
                          {event.description && 
                           !event.description.toLowerCase().includes('created from voice') &&
                           !event.description.toLowerCase().includes('meeting tonight with team') &&
                           !event.description.toLowerCase().includes('doctor check up') &&
                           !event.description.toLowerCase().includes('emergency meeting') &&
                           event.description.trim().length > 0 && (
                            <div className="text-xs text-gray-600 mt-1">
                              <p className="line-clamp-1">{event.description}</p>
                            </div>
                          )}

                          {/* Event Meta - Only show confidence if available */}
                          {event.priority_confidence && (
                            <div className="flex items-center justify-end mt-2 pt-1 border-t border-gray-200 border-opacity-50">
                              <div className="text-xs text-gray-400">
                                {Math.round(event.priority_confidence * 100)}% confidence
                              </div>
                            </div>
                          )}
                        </motion.div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Footer Actions */}
              <div className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-2xl">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-600">
                    {sortedEvents.length} event{sortedEvents.length !== 1 ? 's' : ''} on this day
                  </div>
                  {onCreateEvent && (
                    <button
                      onClick={() => {
                        onCreateEvent(date);
                        onClose();
                      }}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                    >
                      + Add Event
                    </button>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default EventListModal;
