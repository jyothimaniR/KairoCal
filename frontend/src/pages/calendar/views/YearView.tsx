import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import { CalendarDaysIcon } from '@heroicons/react/24/solid';
import type { Event } from '../../../services/apiService';
import { getPriorityInfo } from '../../../utils/priorityUtils';

export interface YearViewProps {
  events: Event[];
  selectedDate: Date;
  onSelectDate: (date: Date) => void;
  onEventClick?: (event: Event) => void;
  onCreateEvent?: (date: Date) => void;
  currentDate: Date;
  onDateChange: (date: Date) => void;
}

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

const DAYS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

const isSameDay = (a: Date, b: Date): boolean =>
  a.getFullYear() === b.getFullYear() && 
  a.getMonth() === b.getMonth() && 
  a.getDate() === b.getDate();

const isSameMonth = (a: Date, b: Date): boolean =>
  a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth();

const getMonthDays = (year: number, month: number): Date[] => {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const startDate = new Date(firstDay);
  const endDate = new Date(lastDay);
  
  // Start from Sunday of the week containing the first day
  startDate.setDate(startDate.getDate() - startDate.getDay());
  
  // End at Saturday of the week containing the last day
  endDate.setDate(endDate.getDate() + (6 - endDate.getDay()));
  
  const days: Date[] = [];
  const currentDate = new Date(startDate);
  
  while (currentDate <= endDate) {
    days.push(new Date(currentDate));
    currentDate.setDate(currentDate.getDate() + 1);
  }
  
  return days;
};

const getEventsForDate = (events: Event[], date: Date): Event[] => {
  return events.filter(event => {
    const eventDate = new Date(event.start_time);
    return isSameDay(eventDate, date);
  });
};

const getEventsForMonth = (events: Event[], year: number, month: number): Event[] => {
  return events.filter(event => {
    const eventDate = new Date(event.start_time);
    return eventDate.getFullYear() === year && eventDate.getMonth() === month;
  });
};

const YearView: React.FC<YearViewProps> = ({
  events,
  selectedDate,
  onSelectDate,
  currentDate,
  onDateChange
}) => {
  const [hoveredMonth, setHoveredMonth] = useState<number | null>(null);
  const [hoveredDate, setHoveredDate] = useState<Date | null>(null);
  
  const today = useMemo(() => new Date(), []);
  const currentYear = currentDate.getFullYear();
  
  // Group events by month for performance
  const eventsByMonth = useMemo(() => {
    const monthEvents: { [key: number]: Event[] } = {};
    for (let i = 0; i < 12; i++) {
      monthEvents[i] = getEventsForMonth(events, currentYear, i);
    }
    return monthEvents;
  }, [events, currentYear]);

  const navigateYear = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    newDate.setFullYear(newDate.getFullYear() + (direction === 'next' ? 1 : -1));
    onDateChange(newDate);
  };

  const goToToday = () => {
    const today = new Date();
    onDateChange(today);
    onSelectDate(today);
  };

  const handleDateClick = (date: Date) => {
    onSelectDate(date);
    // Switch to day view when clicking a date
    onDateChange(date);
  };

  const handleMonthClick = (month: number) => {
    const newDate = new Date(currentYear, month, 1);
    onDateChange(newDate);
    onSelectDate(newDate);
  };

  const renderMonth = (month: number) => {
    const monthDays = getMonthDays(currentYear, month);
    const monthEvents = eventsByMonth[month];
    const isCurrentMonth = isSameMonth(new Date(currentYear, month, 1), today);
    const isSelectedMonth = isSameMonth(new Date(currentYear, month, 1), selectedDate);
    const isHovered = hoveredMonth === month;
    
    return (
      <motion.div
        key={month}
        className={`
          bg-white border border-gray-200 rounded-lg p-4 cursor-pointer
          transition-all duration-200
          ${isSelectedMonth ? 'ring-2 ring-blue-500 shadow-lg' : ''}
          ${isHovered ? 'shadow-md bg-gray-50' : ''}
          hover:shadow-md hover:bg-gray-50
        `}
        onMouseEnter={() => setHoveredMonth(month)}
        onMouseLeave={() => setHoveredMonth(null)}
        whileHover={{ scale: 1.02 }}
        layoutId={`month-${month}`}
      >
        {/* Month header */}
        <div 
          className="flex items-center justify-between mb-3"
          onClick={() => handleMonthClick(month)}
        >
          <h3 className={`
            font-semibold text-sm
            ${isCurrentMonth ? 'text-blue-600' : 'text-gray-900'}
            ${isHovered ? 'text-blue-600' : ''}
          `}>
            {MONTHS[month]}
          </h3>
          {monthEvents.length > 0 && (
            <div className="flex items-center space-x-1">
              <CalendarDaysIcon className="h-3 w-3 text-blue-500" />
              <span className="text-xs text-blue-600 font-medium">
                {monthEvents.length}
              </span>
            </div>
          )}
        </div>
        
        {/* Days of week header */}
        <div className="grid grid-cols-7 gap-1 mb-2">
          {DAYS.map((day, index) => (
            <div
              key={index}
              className="text-center text-xs font-medium text-gray-500 p-1"
            >
              {day}
            </div>
          ))}
        </div>
        
        {/* Calendar grid */}
        <div className="grid grid-cols-7 gap-1">
          {monthDays.map((date, dateIndex) => {
            const isInCurrentMonth = date.getMonth() === month;
            const isToday = isSameDay(date, today);
            const isSelected = isSameDay(date, selectedDate);
            const dayEvents = getEventsForDate(events, date);
            const isDateHovered = hoveredDate && isSameDay(hoveredDate, date);
            
            // Get priority info for the highest priority event
            const highestPriorityEvent = dayEvents.length > 0 
              ? dayEvents.reduce((highest, current) => 
                  (current.priority_level || 1) > (highest.priority_level || 1) ? current : highest
                )
              : null;
            
            const priorityInfo = highestPriorityEvent ? getPriorityInfo(highestPriorityEvent.priority_level) : null;
            
            return (
              <motion.div
                key={dateIndex}
                className={`
                  relative h-6 w-6 text-xs flex items-center justify-center cursor-pointer rounded
                  transition-all duration-200
                  ${!isInCurrentMonth ? 'text-gray-300' : 'text-gray-700'}
                  ${isToday && isInCurrentMonth ? 'bg-blue-100 text-blue-700 font-bold' : ''}
                  ${isSelected && isInCurrentMonth ? 'bg-blue-500 text-white font-semibold' : ''}
                  ${isDateHovered && isInCurrentMonth ? 'bg-gray-200' : ''}
                  ${!isToday && !isSelected && isInCurrentMonth ? 'hover:bg-gray-100' : ''}
                `}
                onClick={(e) => {
                  e.stopPropagation();
                  if (isInCurrentMonth) {
                    handleDateClick(date);
                  }
                }}
                onMouseEnter={() => setHoveredDate(date)}
                onMouseLeave={() => setHoveredDate(null)}
                whileHover={{ scale: isInCurrentMonth ? 1.1 : 1 }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="relative z-10">{date.getDate()}</span>
                
                {/* Event indicators */}
                {dayEvents.length > 0 && isInCurrentMonth && (
                  <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 flex space-x-0.5">
                    {dayEvents.slice(0, 3).map((event, eventIndex) => {
                      const eventPriority = getPriorityInfo(event.priority_level);
                      return (
                        <div
                          key={eventIndex}
                          className={`
                            w-1 h-1 rounded-full
                            ${eventPriority.color === 'red' ? 'bg-red-500' : ''}
                            ${eventPriority.color === 'orange' ? 'bg-orange-500' : ''}
                            ${eventPriority.color === 'blue' ? 'bg-blue-500' : ''}
                            ${eventPriority.color === 'green' ? 'bg-green-500' : ''}
                          `}
                        />
                      );
                    })}
                    {dayEvents.length > 3 && (
                      <div className="w-1 h-1 rounded-full bg-gray-400" />
                    )}
                  </div>
                )}
                
                {/* Priority background for high priority events */}
                {priorityInfo && priorityInfo.color === 'red' && isInCurrentMonth && !isSelected && (
                  <div className="absolute inset-0 bg-red-100 rounded opacity-30" />
                )}
              </motion.div>
            );
          })}
        </div>
        
        {/* Month summary */}
        {monthEvents.length > 0 && isHovered && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 pt-2 border-t border-gray-200"
          >
            <div className="flex items-center justify-between text-xs">
              <span className="text-gray-600">
                {monthEvents.length} event{monthEvents.length !== 1 ? 's' : ''}
              </span>
              <div className="flex space-x-1">
                {['red', 'orange', 'blue', 'green'].map(color => {
                  const count = monthEvents.filter(e => {
                    const priority = getPriorityInfo(e.priority_level);
                    return priority.color === color;
                  }).length;
                  
                  if (count === 0) return null;
                  
                  return (
                    <div
                      key={color}
                      className={`
                        w-2 h-2 rounded-full
                        ${color === 'red' ? 'bg-red-500' : ''}
                        ${color === 'orange' ? 'bg-orange-500' : ''}
                        ${color === 'blue' ? 'bg-blue-500' : ''}
                        ${color === 'green' ? 'bg-green-500' : ''}
                      `}
                      title={`${count} ${color} priority events`}
                    />
                  );
                })}
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>
    );
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Year Header */}
      <div className="flex-shrink-0 flex items-center justify-between p-6 border-b border-gray-200">
        <div className="flex items-center space-x-4">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">
              {currentYear}
            </h2>
            <p className="text-sm text-gray-600">
              {events.filter(e => new Date(e.start_time).getFullYear() === currentYear).length} events this year
            </p>
          </div>
          <button
            onClick={goToToday}
            className="px-4 py-2 text-sm bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors font-medium"
          >
            Today
          </button>
        </div>
        
        <div className="flex items-center space-x-2">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigateYear('prev')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Previous year"
          >
            <ChevronLeftIcon className="h-6 w-6 text-gray-600" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigateYear('next')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Next year"
          >
            <ChevronRightIcon className="h-6 w-6 text-gray-600" />
          </motion.button>
        </div>
      </div>

      {/* Year Grid */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
          {Array.from({ length: 12 }, (_, month) => renderMonth(month))}
        </div>
      </div>

      {/* Year Statistics */}
      <div className="flex-shrink-0 border-t border-gray-200 bg-gray-50 p-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {events.filter(e => new Date(e.start_time).getFullYear() === currentYear).length}
              </div>
              <div className="text-sm text-gray-600">Total Events</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-red-600">
                {events.filter(e => {
                  const priority = getPriorityInfo(e.priority_level);
                  return new Date(e.start_time).getFullYear() === currentYear && priority.color === 'red';
                }).length}
              </div>
              <div className="text-sm text-gray-600">Critical</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-600">
                {events.filter(e => {
                  const priority = getPriorityInfo(e.priority_level);
                  return new Date(e.start_time).getFullYear() === currentYear && priority.color === 'orange';
                }).length}
              </div>
              <div className="text-sm text-gray-600">High Priority</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-600">
                {events.filter(e => {
                  const priority = getPriorityInfo(e.priority_level);
                  return new Date(e.start_time).getFullYear() === currentYear && priority.color === 'blue';
                }).length}
              </div>
              <div className="text-sm text-gray-600">Medium Priority</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default YearView;
