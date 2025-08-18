import React, { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import { PlusIcon, ClockIcon, MapPinIcon } from '@heroicons/react/24/solid';
import type { Event } from '../../../services/apiService';
import { getPriorityInfo } from '../../../utils/priorityUtils';
import EventListModal from '../components/EventListModal';

export interface MonthViewProps {
  events: Event[];
  selectedDate: Date;
  onSelectDate: (date: Date) => void;
  onEventClick?: (event: Event) => void;
  onCreateEvent?: (date: Date) => void;
  currentDate: Date;
  onDateChange: (date: Date) => void;
}

// Helper functions for calendar calculations
const dayKey = (d: Date) => {
  const y = d.getFullYear();
  const m = `${d.getMonth() + 1}`.padStart(2, '0');
  const day = `${d.getDate()}`.padStart(2, '0');
  return `${y}-${m}-${day}`;
};

const startOfMonth = (d: Date) => new Date(d.getFullYear(), d.getMonth(), 1);
const endOfMonth = (d: Date) => new Date(d.getFullYear(), d.getMonth() + 1, 0);
const isSameDay = (a: Date, b: Date) =>
  a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

const formatTime = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });
  } catch {
    return '';
  }
};

const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + '...';
};

const MonthView: React.FC<MonthViewProps> = ({ 
  events, 
  selectedDate, 
  onSelectDate, 
  onEventClick,
  onCreateEvent,
  currentDate,
  onDateChange 
}) => {
  const today = useMemo(() => new Date(), []);
  const [hoveredDate, setHoveredDate] = useState<string | null>(null);
  const [modalDate, setModalDate] = useState<Date | null>(null);
  const [modalEvents, setModalEvents] = useState<Event[]>([]);

  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);
  const startWeekday = monthStart.getDay(); // 0 Sun - 6 Sat
  const daysInMonth = monthEnd.getDate();

  // Group events by day with proper sorting
  const eventsByDay = useMemo(() => {
    const map = new Map<string, Event[]>();
    for (const event of events || []) {
      if (!event.start_time) continue;
      
      const eventDate = new Date(event.start_time);
      const key = dayKey(eventDate);
      
      if (!map.has(key)) {
        map.set(key, []);
      }
      map.get(key)!.push(event);
    }
    
    // Sort events within each day by start time and priority
    map.forEach((dayEvents) => {
      dayEvents.sort((a, b) => {
        // First sort by start time
        const timeCompare = new Date(a.start_time).getTime() - new Date(b.start_time).getTime();
        if (timeCompare !== 0) return timeCompare;
        
        // Then by priority (lower number = higher priority)
        const aPriority = a.priority_level || 3;
        const bPriority = b.priority_level || 3;
        return aPriority - bPriority;
      });
    });
    
    return map;
  }, [events]);

  // Generate calendar grid (42 cells for 6 weeks)
  const gridDays: Array<{ date: Date; inMonth: boolean }> = useMemo(() => {
    const days: Array<{ date: Date; inMonth: boolean }> = [];
    
    // Leading days from previous month
    for (let i = 0; i < startWeekday; i++) {
      const d = new Date(monthStart);
      d.setDate(d.getDate() - (startWeekday - i));
      days.push({ date: d, inMonth: false });
    }
    
    // Current month days
    for (let i = 1; i <= daysInMonth; i++) {
      days.push({ 
        date: new Date(currentDate.getFullYear(), currentDate.getMonth(), i), 
        inMonth: true 
      });
    }
    
    // Trailing days to complete grid (42 total cells)
    while (days.length < 42) {
      const last = days[days.length - 1].date;
      const d = new Date(last);
      d.setDate(d.getDate() + 1);
      days.push({ date: d, inMonth: false });
    }
    
    return days;
  }, [currentDate, monthStart, startWeekday, daysInMonth]);

  const monthName = currentDate.toLocaleString(undefined, { month: 'long' });
  const year = currentDate.getFullYear();

  const navigateMonth = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    newDate.setMonth(newDate.getMonth() + (direction === 'next' ? 1 : -1));
    onDateChange(newDate);
  };

  const goToToday = () => {
    onDateChange(new Date());
    onSelectDate(new Date());
  };

  const handleDateClick = (date: Date, dayEvents: Event[]) => {
    onSelectDate(date);
    
    // If there are events, show the modal
    if (dayEvents.length > 0) {
      setModalDate(date);
      setModalEvents(dayEvents);
    }
  };

  const handleMoreClick = (date: Date, dayEvents: Event[], e: React.MouseEvent) => {
    e.stopPropagation();
    setModalDate(date);
    setModalEvents(dayEvents);
  };

  const closeModal = () => {
    setModalDate(null);
    setModalEvents([]);
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Month Header */}
      <div className="flex-shrink-0 flex items-center justify-between p-6 border-b border-gray-200">
        <div className="flex items-center space-x-4">
          <h2 className="text-2xl font-bold text-gray-900">
            {monthName} {year}
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
            onClick={() => navigateMonth('prev')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Previous month"
          >
            <ChevronLeftIcon className="h-5 w-5 text-gray-600" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigateMonth('next')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Next month"
          >
            <ChevronRightIcon className="h-5 w-5 text-gray-600" />
          </motion.button>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Day Headers */}
        <div className="flex-shrink-0 grid grid-cols-7 border-b border-gray-200">
          {['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map((day) => (
            <div 
              key={day} 
              className="p-3 text-center text-sm font-semibold text-gray-700 bg-gray-50"
            >
              <span className="hidden sm:block">{day}</span>
              <span className="sm:hidden">{day.substring(0, 3)}</span>
            </div>
          ))}
        </div>

        {/* Calendar Days Grid */}
        <div className="flex-1 grid grid-cols-7 grid-rows-6 gap-0 overflow-hidden">
          {gridDays.map(({ date, inMonth }) => {
            const key = dayKey(date);
            const dayEvents = eventsByDay.get(key) || [];
            const isToday = isSameDay(date, today);
            const isSelected = isSameDay(date, selectedDate);
            const isHovered = hoveredDate === key;
            
            return (
              <motion.div
                key={key}
                className={`
                  relative border-r border-b border-gray-200 cursor-pointer
                  ${inMonth ? 'bg-white' : 'bg-gray-50'}
                  ${isToday ? 'bg-blue-50' : ''}
                  ${isSelected ? 'ring-2 ring-blue-500 ring-inset' : ''}
                  hover:bg-gray-50 transition-colors
                `}
                onMouseEnter={() => setHoveredDate(key)}
                onMouseLeave={() => setHoveredDate(null)}
                onClick={() => handleDateClick(date, dayEvents)}
                whileHover={{ scale: 1.01 }}
              >
                {/* Date Number */}
                <div className="p-2">
                  <div className={`
                    inline-flex items-center justify-center w-7 h-7 text-sm rounded-full
                    ${isToday ? 'bg-blue-600 text-white font-bold' : ''}
                    ${!inMonth ? 'text-gray-400' : 'text-gray-900'}
                    ${isSelected && !isToday ? 'bg-gray-200' : ''}
                  `}>
                    {date.getDate()}
                  </div>
                </div>

                {/* Events Display */}
                <div className="px-2 pb-2 space-y-1 overflow-hidden">
                  {dayEvents.slice(0, 3).map((event, index) => {
                    const priority = getPriorityInfo(event.priority_level);
                    const isAllDay = event.all_day || event.is_all_day;
                    
                    return (
                      <motion.div
                        key={`${event.id}-${index}`}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                        onClick={(e) => {
                          e.stopPropagation();
                          onEventClick?.(event);
                        }}
                        className={`
                          group text-xs p-1 rounded cursor-pointer
                          ${priority.bgColor} ${priority.textColor}
                          hover:shadow-sm transition-all duration-200
                          border-l-2 border-${priority.color}-400
                        `}
                        whileHover={{ scale: 1.02, x: 2 }}
                      >
                        <div className="flex items-center space-x-1">
                          {!isAllDay && (
                            <ClockIcon className="h-3 w-3 flex-shrink-0 opacity-70" />
                          )}
                          <span className="font-medium truncate">
                            {truncateText(event.title, 15)}
                          </span>
                        </div>
                        {!isAllDay && (
                          <div className="flex items-center mt-0.5 opacity-75">
                            <span className="text-xs">
                              {formatTime(event.start_time)}
                            </span>
                            {event.location && (
                              <>
                                <MapPinIcon className="h-2.5 w-2.5 ml-1 mr-0.5" />
                                <span className="truncate text-xs">
                                  {truncateText(event.location, 10)}
                                </span>
                              </>
                            )}
                          </div>
                        )}
                      </motion.div>
                    );
                  })}
                  
                  {/* More events indicator */}
                  {dayEvents.length > 3 && (
                    <motion.button
                      onClick={(e) => handleMoreClick(date, dayEvents, e)}
                      className="text-xs text-blue-600 hover:text-blue-800 px-2 py-1 hover:bg-blue-50 rounded transition-colors font-medium"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      +{dayEvents.length - 3} more
                    </motion.button>
                  )}
                </div>

                {/* Add Event Button (on hover) */}
                <AnimatePresence>
                  {isHovered && onCreateEvent && (
                    <motion.button
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      onClick={(e) => {
                        e.stopPropagation();
                        onCreateEvent(date);
                      }}
                      className="absolute top-2 right-2 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors shadow-md"
                      title={`Add event for ${date.toDateString()}`}
                    >
                      <PlusIcon className="h-3 w-3" />
                    </motion.button>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Calendar Legend */}
      <div className="flex-shrink-0 border-t border-gray-200 px-6 py-3 bg-gray-50">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">Priority Levels:</span>
            <div className="flex space-x-2">
              {[1, 2, 3, 4, 5].map((level) => {
                const info = getPriorityInfo(level);
                return (
                  <div key={level} className="flex items-center space-x-1">
                    <div className={`w-3 h-3 rounded ${info.bgColor} border-l-2 border-${info.color}-400`}></div>
                    <span className="text-gray-600">{info.label}</span>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="text-gray-500">
            Click dates to select • Click events to view details • Hover to add events
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

export default MonthView;
