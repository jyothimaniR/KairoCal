import React, { useMemo, useState, useRef, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import { PlusIcon, ClockIcon, MapPinIcon, UserIcon, DocumentTextIcon } from '@heroicons/react/24/solid';
import type { Event } from '../../../services/apiService';
import { apiService } from '../../../services/apiService';
import { getPriorityInfo } from '../../../utils/priorityUtils';
import { useDragAndDrop } from '../hooks/useDragAndDrop';
import DragPreview from '../components/DragPreview';
import EventListModal from '../components/EventListModal';

export interface DayViewProps {
  events: Event[];
  selectedDate: Date;
  onSelectDate: (date: Date) => void;
  onEventClick?: (event: Event) => void;
  onCreateEvent?: (date: Date) => void;
  onEventUpdate?: () => void; // Callback to refresh events after drag & drop
  currentDate: Date;
  onDateChange: (date: Date) => void;
}

const formatTime = (hour: number): string => {
  if (hour === 0) return '12:00 AM';
  if (hour < 12) return `${hour}:00 AM`;
  if (hour === 12) return '12:00 PM';
  return `${hour - 12}:00 PM`;
};

const formatTimeSlot = (hour: number, minute: number): string => {
  const period = hour < 12 ? 'AM' : 'PM';
  const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
  return `${displayHour}:${minute.toString().padStart(2, '0')} ${period}`;
};

const getEventPosition = (event: Event): { top: number; height: number } => {
  const start = new Date(event.start_time);
  const end = new Date(event.end_time);
  
  const startMinutes = start.getHours() * 60 + start.getMinutes();
  const endMinutes = end.getHours() * 60 + end.getMinutes();
  const duration = Math.max(endMinutes - startMinutes, 30); // Minimum 30 minutes
  
  // Fixed positioning: Each hour is exactly 80px, so each minute is 80/60 = 1.333px
  const pixelsPerMinute = 80 / 60;
  
  // Position from top of the fixed container (0 = midnight)
  const top = startMinutes * pixelsPerMinute;
  const height = duration * pixelsPerMinute;
  
  return {
    top: Math.max(top, 0),
    height: Math.max(height, 40) // Minimum 40px height for readability
  };
};

const isSameDay = (a: Date, b: Date): boolean =>
  a.getFullYear() === b.getFullYear() && 
  a.getMonth() === b.getMonth() && 
  a.getDate() === b.getDate();

const DayView: React.FC<DayViewProps> = ({
  events,
  // selectedDate, // unused
  onSelectDate,
  onEventClick,
  onCreateEvent,
  onEventUpdate,
  currentDate,
  onDateChange
}) => {
  const [hoveredSlot, setHoveredSlot] = useState<{hour: number, minute: number} | null>(null);
  const [modalDate, setModalDate] = useState<Date | null>(null);
  const [modalEvents, setModalEvents] = useState<Event[]>([]);
  const dayContainerRef = useRef<HTMLDivElement>(null);
  const recentDragEndRef = useRef<number>(0); // Track when drag ended
  
  const today = useMemo(() => new Date(), []);

  // Drag and drop functionality
  const handleEventMove = useCallback(async (
    eventId: string,
    newStartTime: Date,
    newEndTime: Date
  ): Promise<boolean> => {
    try {
      console.log('🔄 Moving event:', eventId);
      console.log('📅 New start time (local):', newStartTime);
      console.log('📅 New end time (local):', newEndTime);
      
      // Format dates for backend (YYYY-MM-DDTHH:mm:ss format without timezone conversion)
      const formatForBackend = (date: Date): string => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        
        return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
      };
      
      const startTimeFormatted = formatForBackend(newStartTime);
      const endTimeFormatted = formatForBackend(newEndTime);
      
      console.log('📅 Formatted start time for backend:', startTimeFormatted);
      console.log('📅 Formatted end time for backend:', endTimeFormatted);
      
      const success = await apiService.updateEvent(eventId, {
        start_time: startTimeFormatted,
        end_time: endTimeFormatted,
      });

      if (success && onEventUpdate) {
        onEventUpdate(); // Refresh events
      }

      return !!success; // Convert Event | null to boolean
    } catch (error) {
      console.error('Failed to update event:', error);
      return false;
    }
  }, [onEventUpdate]);

  const {
    dragState,
    handleDragStart,
    handleDragMove,
    handleDragEnd: originalHandleDragEnd,
    handleDragCancel,
  } = useDragAndDrop(events, handleEventMove);

  // Wrapper for handleDragEnd to track drag completion
  const handleDragEnd = useCallback(async (container: HTMLElement | null, date: Date) => {
    if (!container) return false; // Handle null case
    const result = await originalHandleDragEnd(container, date);
    recentDragEndRef.current = Date.now(); // Record when drag ended
    return result;
  }, [originalHandleDragEnd]);

  // Mouse event handlers for drag and drop
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (dragState.isDragging && dayContainerRef.current) {
        handleDragMove(e, dayContainerRef.current, currentDate);
      }
    };

    const handleMouseUp = async (_e: MouseEvent) => {
      if (dragState.isDragging && dayContainerRef.current) {
        await handleDragEnd(dayContainerRef.current, currentDate);
      }
    };

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && dragState.isDragging) {
        handleDragCancel();
      }
    };

    if (dragState.isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [dragState.isDragging, handleDragMove, handleDragEnd, handleDragCancel, currentDate]);
  
  // Filter events for the current day
  const dayEvents = useMemo(() => {
    return events.filter(event => {
      const eventDate = new Date(event.start_time);
      return isSameDay(eventDate, currentDate);
    }).sort((a, b) => 
      new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
    );
  }, [events, currentDate]);

  const allDayEvents = dayEvents.filter(e => e.all_day || e.is_all_day);
  const timedEvents = dayEvents.filter(e => !e.all_day && !e.is_all_day);

  // Generate 24 hours with 30-minute slots
  const timeSlots = useMemo(() => {
    const slots = [];
    for (let hour = 0; hour < 24; hour++) {
      slots.push({ hour, minute: 0 });
      slots.push({ hour, minute: 30 });
    }
    return slots;
  }, []);

  const navigateDay = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    newDate.setDate(newDate.getDate() + (direction === 'next' ? 1 : -1));
    onDateChange(newDate);
  };

  const goToToday = () => {
    const today = new Date();
    onDateChange(today);
    onSelectDate(today);
  };

  const handleTimeSlotClick = (hour: number, minute: number) => {
    const clickDate = new Date(currentDate);
    clickDate.setHours(hour, minute, 0, 0);
    
    onSelectDate(clickDate);
    
    if (onCreateEvent) {
      onCreateEvent(clickDate);
    }
  };

  const handleEventClick = (event: Event, e: React.MouseEvent) => {
    e.stopPropagation();
    
    // Don't open modal if currently dragging or if drag just ended (within 200ms)
    if (dragState.isDragging || (Date.now() - recentDragEndRef.current < 200)) {
      console.log('🚫 Blocking event click - drag in progress or just ended');
      return;
    }
    
    // Track if this might be a drag operation
    let isDragOperation = false;
    
    // Start drag operation if mouse is held down
    if (e.button === 0 && dayContainerRef.current) { // Left mouse button
      const startDrag = () => {
        isDragOperation = true;
        handleDragStart(event, e, dayContainerRef.current!);
      };
      
      // Small delay to differentiate between click and drag
      const dragTimer = setTimeout(startDrag, 150);
      
      const cleanup = () => {
        clearTimeout(dragTimer);
        document.removeEventListener('mouseup', cleanup);
        document.removeEventListener('mousemove', cleanup);
        
        // Only open modal if it wasn't a drag operation and no recent drag
        if (!isDragOperation && !dragState.isDragging && onEventClick && 
            (Date.now() - recentDragEndRef.current > 200)) {
          console.log('✅ Opening event modal - valid click');
          onEventClick(event);
        }
      };
      
      document.addEventListener('mouseup', cleanup, { once: true });
      document.addEventListener('mousemove', cleanup, { once: true });
    } else {
      // Right click or other buttons - open modal immediately (if no recent drag)
      if (onEventClick && (Date.now() - recentDragEndRef.current > 200)) {
        onEventClick(event);
      }
    }
  };

  // const handleAllDayClick = () => {
  //   if (allDayEvents.length > 0) {
  //     setModalDate(currentDate);
  //     setModalEvents(allDayEvents);
  //   }
  // };

  const closeModal = () => {
    setModalDate(null);
    setModalEvents([]);
  };

  const dayName = currentDate.toLocaleDateString(undefined, { weekday: 'long' });
  const dateStr = currentDate.toLocaleDateString(undefined, { 
    month: 'long', 
    day: 'numeric',
    year: 'numeric'
  });

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Day Header */}
      <div className="flex-shrink-0 flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {dayName}
            </h2>
            <p className="text-sm text-gray-600">{dateStr}</p>
          </div>
          <button
            onClick={goToToday}
            className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors"
          >
            Today
          </button>
        </div>
        
        <div className="flex items-center space-x-2">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigateDay('prev')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Previous day"
          >
            <ChevronLeftIcon className="h-5 w-5 text-gray-600" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigateDay('next')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Next day"
          >
            <ChevronRightIcon className="h-5 w-5 text-gray-600" />
          </motion.button>
        </div>
      </div>

      {/* All-Day Events Section */}
      {allDayEvents.length > 0 && (
        <div className="flex-shrink-0 border-b border-gray-200 bg-gray-50">
          <div className="p-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-semibold text-gray-700">All Day</h3>
              <span className="text-xs text-gray-500">
                {allDayEvents.length} event{allDayEvents.length !== 1 ? 's' : ''}
              </span>
            </div>
            <div className="grid gap-2">
              {allDayEvents.map((event, index) => {
                const priority = getPriorityInfo(event.priority_level);
                
                return (
                  <motion.div
                    key={`${event.id}-allday-${index}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    onClick={(e) => handleEventClick(event, e)}
                    className={`
                      p-3 rounded-lg cursor-pointer border-l-4
                      ${priority.bgColor} ${priority.textColor} border-${priority.color}-400
                      hover:shadow-md transition-all duration-200
                    `}
                    whileHover={{ scale: 1.02, x: 4 }}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-semibold text-sm">{event.title}</h4>
                        {event.description && (
                          <p className="text-xs opacity-75 mt-1 line-clamp-2">
                            {event.description}
                          </p>
                        )}
                        {event.location && (
                          <div className="flex items-center space-x-1 mt-1 text-xs opacity-75">
                            <MapPinIcon className="h-3 w-3" />
                            <span>{event.location}</span>
                          </div>
                        )}
                      </div>
                      <div className="flex flex-col items-end space-y-1">
                        <span className="text-xs px-2 py-1 bg-white bg-opacity-50 rounded">
                          {priority.label}
                        </span>
                        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                          All Day
                        </span>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Time Grid - Single scrollable container */}
      <div className="flex-1 overflow-y-auto" ref={dayContainerRef}>
        <div className="flex" style={{ height: '1920px' }}> {/* Fixed 24-hour grid: 24 * 80px */}
          {/* Time Column - Scrolls with the day view */}
          <div className="flex-shrink-0 w-20 border-r border-gray-200 bg-gray-50 relative">
            {Array.from({ length: 24 }, (_, hour) => (
              <div
                key={hour}
                className="absolute h-20 border-b border-gray-200 flex items-start justify-end p-2 w-full"
                style={{ top: `${hour * 80}px` }}
              >
                <span className="text-xs text-gray-600 bg-gray-50 px-1">
                  {formatTime(hour)}
                </span>
              </div>
            ))}
          </div>
          
          {/* Day Column - Events and time slots in unified container */}
          <div className="flex-1 relative">
            {/* Time slots grid - positioned absolutely within container */}
            {timeSlots.map(({ hour, minute }, index) => {
              const isHoured = minute === 0;
              const isHovered = hoveredSlot?.hour === hour && hoveredSlot?.minute === minute;
              const topPosition = (hour * 80) + (minute === 30 ? 40 : 0); // Exact pixel positioning
              
              return (
                <div
                  key={index}
                  className={`
                    absolute w-full h-10 border-gray-200 cursor-pointer
                    ${isHoured ? 'border-b' : 'border-b border-dashed border-opacity-50'}
                    ${isHovered ? 'bg-blue-50' : 'hover:bg-gray-50'}
                    transition-colors
                  `}
                  style={{ top: `${topPosition}px` }}
                  onClick={() => handleTimeSlotClick(hour, minute)}
                  onMouseEnter={() => setHoveredSlot({ hour, minute })}
                  onMouseLeave={() => setHoveredSlot(null)}
                >
                  {/* Time slot label on hover */}
                  <AnimatePresence>
                    {isHovered && (
                      <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="absolute left-2 top-1/2 transform -translate-y-1/2 z-20"
                      >
                        <div className="bg-blue-600 text-white px-2 py-1 rounded text-xs font-medium shadow-md">
                          {formatTimeSlot(hour, minute)}
                          <div className="absolute right-0 top-1/2 transform translate-x-full -translate-y-1/2">
                            <div className="w-2 h-2 bg-blue-600 rotate-45"></div>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                  
                  {/* Add event button on hover */}
                  <AnimatePresence>
                    {isHovered && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        className="absolute right-4 top-1/2 transform -translate-y-1/2 z-10"
                      >
                        <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-blue-600 transition-colors">
                          <PlusIcon className="h-4 w-4" />
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              );
            })}
            
            {/* Current time indicator - only show if viewing today */}
            {isSameDay(currentDate, today) && (() => {
              const now = new Date();
              const currentMinutes = now.getHours() * 60 + now.getMinutes();
              const currentTimeTop = currentMinutes * (80 / 60); // Convert to pixel position
              
              return (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="absolute left-0 right-0 z-30 pointer-events-none"
                  style={{ top: `${currentTimeTop}px` }}
                >
                  {/* Red line indicator */}
                  <div className="h-0.5 bg-red-500 shadow-sm">
                    {/* Red circle at the beginning */}
                    <div className="absolute -left-2 -top-1.5 w-3 h-3 bg-red-500 rounded-full border-2 border-white shadow-md"></div>
                  </div>
                  {/* Current time label */}
                  <div className="absolute -left-16 -top-3 text-xs text-red-500 font-semibold bg-white px-1 rounded shadow-sm">
                    {now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })}
                  </div>
                </motion.div>
              );
            })()}
            
            {/* Events positioned absolutely within container */}
            {timedEvents.map((event, eventIndex) => {
              const priority = getPriorityInfo(event.priority_level);
              const position = getEventPosition(event);
              const eventStart = new Date(event.start_time);
              const eventEnd = new Date(event.end_time);
              const duration = Math.round((eventEnd.getTime() - eventStart.getTime()) / (1000 * 60));
              
              return (
                <motion.div
                  key={`${event.id}-timed-${eventIndex}`}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className={`
                    absolute rounded-lg shadow-sm border-l-4
                    ${priority.bgColor} ${priority.textColor} border-${priority.color}-400
                    cursor-grab hover:cursor-grab active:cursor-grabbing
                    hover:shadow-lg transition-all
                    overflow-hidden z-10
                    ${dragState.draggedEvent?.id === event.id ? 'opacity-50' : 'hover:scale-105'}
                  `}
                  style={{
                    top: `${position.top}px`,
                    height: `${position.height}px`,
                    left: '8px',
                    right: '8px'
                  }}
                  onClick={(e) => handleEventClick(event, e)}
                  onMouseDown={(e) => {
                    if (e.button === 0) { // Left mouse button
                      e.preventDefault(); // Prevent text selection
                    }
                  }}
                  whileHover={{ x: dragState.isDragging ? 0 : 4 }}
                  drag={false} // We handle drag manually for better control
                >
                  <div className="p-3 h-full flex flex-col">
                    {/* Event header */}
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-sm leading-tight flex-1 pr-2">
                        {event.title}
                      </h4>
                      <span className="text-xs px-2 py-1 bg-white bg-opacity-50 rounded flex-shrink-0">
                        {priority.label}
                      </span>
                    </div>
                    
                    {/* Event time */}
                    <div className="flex items-center space-x-1 text-xs opacity-90 mb-2">
                      <ClockIcon className="h-3 w-3 flex-shrink-0" />
                      <span>
                        {eventStart.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })}
                        {' - '}
                        {eventEnd.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })}
                      </span>
                      <span className="text-xs opacity-75">({duration} min)</span>
                    </div>
                    
                    {/* Event location */}
                    {event.location && (
                      <div className="flex items-center space-x-1 text-xs opacity-75 mb-2">
                        <MapPinIcon className="h-3 w-3 flex-shrink-0" />
                        <span className="truncate">{event.location}</span>
                      </div>
                    )}
                    
                    {/* Event description */}
                    {event.description && position.height > 80 && (
                      <div className="flex-1 overflow-hidden">
                        <div className="flex items-start space-x-1 text-xs opacity-75">
                          <DocumentTextIcon className="h-3 w-3 flex-shrink-0 mt-0.5" />
                          <p className="line-clamp-3 text-xs leading-relaxed">
                            {event.description}
                          </p>
                        </div>
                      </div>
                    )}
                    
                    {/* Event metadata */}
                    {position.height > 120 && (
                      <div className="mt-2 pt-2 border-t border-white border-opacity-30">
                        <div className="flex items-center justify-between text-xs">
                          {event.created_via && (
                            <div className="flex items-center space-x-1">
                              <UserIcon className="h-3 w-3 opacity-50" />
                              <span className="opacity-75 capitalize">{event.created_via}</span>
                            </div>
                          )}
                          {event.priority_confidence && (
                            <span className="opacity-50">
                              {Math.round(event.priority_confidence * 100)}% confidence
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Drag Preview */}
      <DragPreview
        isDragging={dragState.isDragging}
        draggedEvent={dragState.draggedEvent}
        previewTime={dragState.previewTime}
        conflictingEvents={dragState.conflictingEvents}
        position={dragState.currentPosition}
      />

      {/* Event List Modal */}
      <EventListModal
        isOpen={modalDate !== null}
        onClose={closeModal}
        date={modalDate || new Date()}
        events={modalEvents}
        onEventClick={onEventClick}
        onCreateEvent={onCreateEvent}
      />
    </div>
  );
};

export default DayView;
