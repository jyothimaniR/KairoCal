import React, { useMemo, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import { PlusIcon, ClockIcon, MapPinIcon } from '@heroicons/react/24/solid';
import type { Event } from '../../../services/apiService';
import { getPriorityInfo } from '../../../utils/priorityUtils';
import EventListModal from '../components/EventListModal';

export interface WeekViewProps {
  events: Event[];
  selectedDate: Date;
  onSelectDate: (date: Date) => void;
  onEventClick?: (event: Event) => void;
  onCreateEvent?: (date: Date) => void;
  currentDate: Date;
  onDateChange: (date: Date) => void;
}

// Helper functions for week calculations
const getWeekStart = (date: Date): Date => {
  const start = new Date(date);
  start.setDate(start.getDate() - start.getDay()); // Sunday
  start.setHours(0, 0, 0, 0);
  return start;
};

const getWeekEnd = (date: Date): Date => {
  const end = new Date(getWeekStart(date));
  end.setDate(end.getDate() + 6);
  end.setHours(23, 59, 59, 999);
  return end;
};

const formatTime = (hour: number): string => {
  if (hour === 0) return '12 AM';
  if (hour < 12) return `${hour} AM`;
  if (hour === 12) return '12 PM';
  return `${hour - 12} PM`;
};

const getEventPosition = (event: Event, startHour: number = 6): { top: number; height: number; left: number; width: number } => {
  const start = new Date(event.start_time);
  const end = new Date(event.end_time);
  
  const startMinutes = start.getHours() * 60 + start.getMinutes();
  const endMinutes = end.getHours() * 60 + end.getMinutes();
  const duration = endMinutes - startMinutes;
  
  // Each hour slot is 64px (16 * 4), so each minute is ~1.07px
  const pixelsPerMinute = 64 / 60; // 1.067px per minute
  const top = (startMinutes - startHour * 60) * pixelsPerMinute;
  const height = Math.max(duration * pixelsPerMinute, 20); // Minimum 20px height
  
  return {
    top: Math.max(top, 0),
    height: Math.min(height, 60), // Maximum height per slot
    left: 0,
    width: 100
  };
};

const isSameDay = (a: Date, b: Date): boolean =>
  a.getFullYear() === b.getFullYear() && 
  a.getMonth() === b.getMonth() && 
  a.getDate() === b.getDate();

const WeekView: React.FC<WeekViewProps> = ({
  events,
  selectedDate,
  onSelectDate,
  onEventClick,
  onCreateEvent,
  currentDate,
  onDateChange
}) => {
  const [hoveredSlot, setHoveredSlot] = useState<{day: number, hour: number} | null>(null);
  const [modalDate, setModalDate] = useState<Date | null>(null);
  const [modalEvents, setModalEvents] = useState<Event[]>([]);
  const weekContainerRef = useRef<HTMLDivElement>(null);
  
  const today = useMemo(() => new Date(), []);
  const weekStart = getWeekStart(currentDate);
  const weekEnd = getWeekEnd(currentDate);
  
  // Generate week days (Sunday to Saturday)
  const weekDays = useMemo(() => {
    const days = [];
    for (let i = 0; i < 7; i++) {
      const day = new Date(weekStart);
      day.setDate(day.getDate() + i);
      days.push(day);
    }
    return days;
  }, [weekStart]);

  // Group events by day
  const eventsByDay = useMemo(() => {
    const map = new Map<string, Event[]>();
    
    weekDays.forEach(day => {
      const dayKey = day.toDateString();
      map.set(dayKey, []);
    });
    
    events.forEach(event => {
      const eventDate = new Date(event.start_time);
      const dayKey = eventDate.toDateString();
      
      if (map.has(dayKey)) {
        map.get(dayKey)!.push(event);
      }
    });
    
    // Sort events within each day by start time
    map.forEach(dayEvents => {
      dayEvents.sort((a, b) => 
        new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
      );
    });
    
    return map;
  }, [events, weekDays]);

  // Hours to display (6 AM to 11 PM)
  const hours = useMemo(() => {
    const hourList = [];
    for (let i = 6; i <= 23; i++) {
      hourList.push(i);
    }
    return hourList;
  }, []);

  const navigateWeek = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    newDate.setDate(newDate.getDate() + (direction === 'next' ? 7 : -7));
    onDateChange(newDate);
  };

  const goToToday = () => {
    const today = new Date();
    onDateChange(today);
    onSelectDate(today);
  };

  const handleTimeSlotClick = (day: Date, hour: number) => {
    const clickDate = new Date(day);
    clickDate.setHours(hour, 0, 0, 0);
    
    onSelectDate(clickDate);
    
    if (onCreateEvent) {
      onCreateEvent(clickDate);
    }
  };

  const handleEventClick = (event: Event, e: React.MouseEvent) => {
    e.stopPropagation();
    if (onEventClick) {
      onEventClick(event);
    }
  };

  const handleDayHeaderClick = (day: Date) => {
    const dayEvents = eventsByDay.get(day.toDateString()) || [];
    if (dayEvents.length > 0) {
      setModalDate(day);
      setModalEvents(dayEvents);
    }
    onSelectDate(day);
  };

  const closeModal = () => {
    setModalDate(null);
    setModalEvents([]);
  };

  const weekRange = `${weekStart.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} - ${weekEnd.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}`;

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Week Header */}
      <div className="flex-shrink-0 flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-4">
          <h2 className="text-2xl font-bold text-gray-900">
            {weekRange}
          </h2>
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
            onClick={() => navigateWeek('prev')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Previous week"
          >
            <ChevronLeftIcon className="h-5 w-5 text-gray-600" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigateWeek('next')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Next week"
          >
            <ChevronRightIcon className="h-5 w-5 text-gray-600" />
          </motion.button>
        </div>
      </div>

      {/* Week Grid */}
      <div className="flex-1 flex flex-col overflow-hidden" ref={weekContainerRef}>
        {/* Day Headers */}
        <div className="flex-shrink-0 grid grid-cols-8 border-b border-gray-200">
          {/* Time column header */}
          <div className="p-3 text-center text-sm font-semibold text-gray-700 bg-gray-50 border-r border-gray-200">
            Time
          </div>
          
          {/* Day headers */}
          {weekDays.map((day, index) => {
            const isToday = isSameDay(day, today);
            const isSelected = isSameDay(day, selectedDate);
            const dayEvents = eventsByDay.get(day.toDateString()) || [];
            
            return (
              <button
                key={index}
                onClick={() => handleDayHeaderClick(day)}
                className={`
                  p-3 text-center border-r border-gray-200 hover:bg-gray-50 transition-colors
                  ${isToday ? 'bg-blue-50' : 'bg-gray-50'}
                  ${isSelected ? 'ring-2 ring-blue-500 ring-inset' : ''}
                `}
              >
                <div className="text-sm font-semibold text-gray-700">
                  {day.toLocaleDateString(undefined, { weekday: 'short' })}
                </div>
                <div className={`text-lg font-bold mt-1 ${isToday ? 'text-blue-600' : 'text-gray-900'}`}>
                  {day.getDate()}
                </div>
                {dayEvents.length > 0 && (
                  <div className="text-xs text-blue-600 mt-1">
                    {dayEvents.length} event{dayEvents.length !== 1 ? 's' : ''}
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Time Grid */}
        <div className="flex-1 overflow-y-auto">
          <div className="grid grid-cols-8">
            {/* Time Column */}
            <div className="border-r border-gray-200 bg-gray-50">
              {/* All-day events row header */}
              <div className="h-12 p-2 text-xs text-gray-600 border-b border-gray-200 flex items-center justify-end">
                All Day
              </div>
              
              {/* Hour rows */}
              {hours.map(hour => (
                <div
                  key={hour}
                  className="h-16 p-2 text-xs text-gray-600 border-b border-gray-200 flex items-start justify-end"
                >
                  {formatTime(hour)}
                </div>
              ))}
            </div>
            
            {/* Day Columns */}
            {weekDays.map((day, dayIndex) => {
              const dayKey = day.toDateString();
              const dayEvents = eventsByDay.get(dayKey) || [];
              const allDayEvents = dayEvents.filter(e => e.all_day || e.is_all_day);
              const timedEvents = dayEvents.filter(e => !e.all_day && !e.is_all_day);
              
              return (
                <div
                  key={dayIndex}
                  className="relative border-r border-gray-200"
                >
                  {/* All-day events row */}
                  <div className="h-12 border-b border-gray-200 bg-gray-50 p-1 relative">
                    {allDayEvents.map((event, eventIndex) => {
                      const priority = getPriorityInfo(event.priority_level);
                      
                      return (
                        <motion.div
                          key={`${event.id}-allday-${eventIndex}`}
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className={`
                            absolute left-1 right-1 h-7 p-1 rounded text-xs font-medium
                            ${priority.bgColor} ${priority.textColor}
                            border-l-4 border-${priority.color}-400
                            cursor-pointer hover:shadow-md transition-shadow
                            flex items-center
                          `}
                          style={{ top: `${eventIndex * 8 + 1}px` }}
                          onClick={(e) => handleEventClick(event, e)}
                          whileHover={{ scale: 1.02 }}
                        >
                          <span className="truncate flex-1">{event.title}</span>
                          <span className="text-xs opacity-75 ml-2">All Day</span>
                        </motion.div>
                      );
                    })}
                    
                    {/* All-day events overflow indicator */}
                    {allDayEvents.length > 1 && (
                      <div className="absolute bottom-0 right-1 text-xs text-gray-500">
                        {allDayEvents.length} all-day
                      </div>
                    )}
                  </div>
                  
                  {/* Hour slots */}
                  {hours.map(hour => {
                    const isHovered = hoveredSlot?.day === dayIndex && hoveredSlot?.hour === hour;
                    
                    return (
                      <div
                        key={hour}
                        className={`
                          h-16 border-b border-gray-200 cursor-pointer relative
                          ${isHovered ? 'bg-blue-50' : 'hover:bg-gray-50'}
                          transition-colors
                        `}
                        onClick={() => handleTimeSlotClick(day, hour)}
                        onMouseEnter={() => setHoveredSlot({ day: dayIndex, hour })}
                        onMouseLeave={() => setHoveredSlot(null)}
                      >
                        {/* Add event button on hover */}
                        <AnimatePresence>
                          {isHovered && (
                            <motion.div
                              initial={{ opacity: 0, scale: 0.8 }}
                              animate={{ opacity: 1, scale: 1 }}
                              exit={{ opacity: 0, scale: 0.8 }}
                              className="absolute inset-0 flex items-center justify-center"
                            >
                              <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-md">
                                <PlusIcon className="h-3 w-3" />
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}
                  
                  {/* Timed Events for this day */}
                  <div className="absolute inset-0 pointer-events-none" style={{ top: '48px' }}>
                    {timedEvents.map((event, eventIndex) => {
                      const priority = getPriorityInfo(event.priority_level);
                      const position = getEventPosition(event, hours[0]);
                      
                      return (
                        <motion.div
                          key={`${event.id}-timed-${eventIndex}`}
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          style={{
                            top: Math.max(position.top, 0),
                            height: Math.max(position.height, 24),
                            left: '4px',
                            right: '4px'
                          }}
                          className={`
                            absolute p-2 rounded-md text-xs
                            ${priority.bgColor} ${priority.textColor}
                            border-l-4 border-${priority.color}-400
                            pointer-events-auto cursor-pointer
                            hover:shadow-lg hover:scale-105 transition-all
                            overflow-hidden
                          `}
                          onClick={(e) => handleEventClick(event, e)}
                          whileHover={{ x: 2 }}
                        >
                          <div className="font-semibold truncate leading-tight">
                            {event.title}
                          </div>
                          <div className="flex items-center space-x-1 text-xs opacity-90 mt-1">
                            <ClockIcon className="h-2.5 w-2.5 flex-shrink-0" />
                            <span className="truncate">
                              {new Date(event.start_time).toLocaleTimeString([], { 
                                hour: 'numeric', 
                                minute: '2-digit',
                                hour12: true 
                              })}
                            </span>
                          </div>
                          {event.location && position.height > 48 && (
                            <div className="flex items-center space-x-1 text-xs opacity-75 mt-1">
                              <MapPinIcon className="h-2.5 w-2.5 flex-shrink-0" />
                              <span className="truncate">{event.location}</span>
                            </div>
                          )}
                        </motion.div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

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

export default WeekView;
