import React from 'react';
import { motion } from 'framer-motion';
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import type { CalendarView } from './ViewSelector';

interface DateNavigationProps {
  currentDate: Date;
  currentView: CalendarView;
  onDateChange: (date: Date) => void;
  onToday: () => void;
}

const DateNavigation: React.FC<DateNavigationProps> = ({ 
  currentDate, 
  currentView, 
  onDateChange, 
  onToday 
}) => {
  const getDisplayText = () => {
    switch (currentView) {
      case 'month':
        return currentDate.toLocaleString(undefined, { month: 'long', year: 'numeric' });
      case 'week':
        const weekStart = new Date(currentDate);
        weekStart.setDate(currentDate.getDate() - currentDate.getDay());
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6);
        
        if (weekStart.getMonth() === weekEnd.getMonth()) {
          return `${weekStart.toLocaleDateString(undefined, { month: 'long' })} ${weekStart.getDate()}-${weekEnd.getDate()}, ${weekStart.getFullYear()}`;
        } else {
          return `${weekStart.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} - ${weekEnd.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}`;
        }
      case 'day':
        return currentDate.toLocaleDateString(undefined, { 
          weekday: 'long', 
          month: 'long', 
          day: 'numeric', 
          year: 'numeric' 
        });
      case 'year':
        return currentDate.getFullYear().toString();
      case 'schedule':
        return 'Upcoming Events';
      default:
        return '';
    }
  };

  const navigatePrev = () => {
    const newDate = new Date(currentDate);
    
    switch (currentView) {
      case 'month':
        newDate.setMonth(newDate.getMonth() - 1);
        break;
      case 'week':
        newDate.setDate(newDate.getDate() - 7);
        break;
      case 'day':
        newDate.setDate(newDate.getDate() - 1);
        break;
      case 'year':
        newDate.setFullYear(newDate.getFullYear() - 1);
        break;
      default:
        return;
    }
    
    onDateChange(newDate);
  };

  const navigateNext = () => {
    const newDate = new Date(currentDate);
    
    switch (currentView) {
      case 'month':
        newDate.setMonth(newDate.getMonth() + 1);
        break;
      case 'week':
        newDate.setDate(newDate.getDate() + 7);
        break;
      case 'day':
        newDate.setDate(newDate.getDate() + 1);
        break;
      case 'year':
        newDate.setFullYear(newDate.getFullYear() + 1);
        break;
      default:
        return;
    }
    
    onDateChange(newDate);
  };

  const isToday = () => {
    const today = new Date();
    return currentDate.toDateString() === today.toDateString();
  };

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <motion.button
          onClick={onToday}
          className={`
            px-4 py-2 text-sm font-medium rounded-lg transition-colors
            ${isToday() 
              ? 'bg-blue-100 text-blue-700 cursor-default' 
              : 'text-gray-700 hover:bg-gray-100'
            }
          `}
          whileHover={!isToday() ? { scale: 1.05 } : {}}
          whileTap={!isToday() ? { scale: 0.95 } : {}}
          disabled={isToday()}
        >
          <CalendarIcon className="h-4 w-4 mr-2 inline" />
          Today
        </motion.button>

        <div className="flex items-center space-x-2">
          <motion.button
            onClick={navigatePrev}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            disabled={currentView === 'schedule'}
          >
            <ChevronLeftIcon className="h-5 w-5 text-gray-600" />
          </motion.button>

          <motion.button
            onClick={navigateNext}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            disabled={currentView === 'schedule'}
          >
            <ChevronRightIcon className="h-5 w-5 text-gray-600" />
          </motion.button>
        </div>
      </div>

      <motion.h1 
        key={getDisplayText()}
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
        className="text-2xl font-bold text-gray-900"
      >
        {getDisplayText()}
      </motion.h1>

      <div className="w-32" /> {/* Spacer for balance */}
    </div>
  );
};

export default DateNavigation;
