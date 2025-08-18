import React, { useMemo, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MagnifyingGlassIcon, 
  // FunnelIcon, // unused 
  CalendarDaysIcon,
  ClockIcon,
  MapPinIcon,
  UserIcon,
  DocumentTextIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';
import { 
  CalendarIcon,
  StarIcon
} from '@heroicons/react/24/solid';
import type { Event } from '../../../services/apiService';
import { getPriorityInfo } from '../../../utils/priorityUtils';

export interface ScheduleViewProps {
  events: Event[];
  selectedDate: Date;
  onSelectDate: (date: Date) => void;
  onEventClick?: (event: Event) => void;
  onCreateEvent?: (date: Date) => void;
  currentDate: Date;
  onDateChange: (date: Date) => void;
}

type SortOption = 'date' | 'priority' | 'title' | 'duration';
type FilterOption = 'all' | 'today' | 'week' | 'month' | 'upcoming';
type PriorityFilter = 'all' | 'critical' | 'high' | 'medium' | 'low';

const SORT_OPTIONS = [
  { value: 'date' as const, label: 'Date & Time', icon: CalendarDaysIcon },
  { value: 'priority' as const, label: 'Priority', icon: StarIcon },
  { value: 'title' as const, label: 'Title', icon: DocumentTextIcon },
  { value: 'duration' as const, label: 'Duration', icon: ClockIcon },
];

const FILTER_OPTIONS = [
  { value: 'all' as const, label: 'All Events', description: 'Show all events' },
  { value: 'today' as const, label: 'Today', description: 'Events happening today' },
  { value: 'week' as const, label: 'This Week', description: 'Next 7 days' },
  { value: 'month' as const, label: 'This Month', description: 'Next 30 days' },
  { value: 'upcoming' as const, label: 'Upcoming', description: 'Future events only' },
];

const PRIORITY_FILTERS = [
  { value: 'all' as const, label: 'All Priorities', color: 'gray' },
  { value: 'critical' as const, label: 'Critical', color: 'red' },
  { value: 'high' as const, label: 'High', color: 'orange' },
  { value: 'medium' as const, label: 'Medium', color: 'blue' },
  { value: 'low' as const, label: 'Low', color: 'green' },
];

const isSameDay = (a: Date, b: Date): boolean =>
  a.getFullYear() === b.getFullYear() && 
  a.getMonth() === b.getMonth() && 
  a.getDate() === b.getDate();

const isWithinDays = (date: Date, days: number): boolean => {
  const now = new Date();
  const diffTime = date.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays >= 0 && diffDays <= days;
};

const formatEventDate = (date: Date): string => {
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  if (isSameDay(date, today)) return 'Today';
  if (isSameDay(date, tomorrow)) return 'Tomorrow';
  
  const diffTime = date.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays > 0 && diffDays <= 7) {
    return `In ${diffDays} day${diffDays === 1 ? '' : 's'}`;
  }
  
  return date.toLocaleDateString(undefined, { 
    weekday: 'short',
    month: 'short', 
    day: 'numeric',
    year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
  });
};

const formatEventTime = (start: Date, end: Date): string => {
  const startTime = start.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });
  const endTime = end.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });
  return `${startTime} - ${endTime}`;
};

const getDuration = (start: Date, end: Date): string => {
  const diffMs = end.getTime() - start.getTime();
  const diffMinutes = Math.round(diffMs / (1000 * 60));
  
  if (diffMinutes < 60) return `${diffMinutes}m`;
  
  const hours = Math.floor(diffMinutes / 60);
  const minutes = diffMinutes % 60;
  
  return minutes === 0 ? `${hours}h` : `${hours}h ${minutes}m`;
};

const ScheduleView: React.FC<ScheduleViewProps> = ({
  events,
  // selectedDate, // unused
  // onSelectDate, // unused
  onEventClick,
  onCreateEvent,
  // currentDate, // unused
  // onDateChange // unused
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('date');
  const [filterBy, setFilterBy] = useState<FilterOption>('upcoming');
  const [priorityFilter, setPriorityFilter] = useState<PriorityFilter>('all');
  const [sortAscending, setSortAscending] = useState(true);
  const [expandedEvent, setExpandedEvent] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  
  const today = useMemo(() => new Date(), []);
  
  // Filter and sort events
  const filteredAndSortedEvents = useMemo(() => {
    let filtered = [...events];
    
    // Apply text search
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(event =>
        event.title.toLowerCase().includes(query) ||
        event.description?.toLowerCase().includes(query) ||
        event.location?.toLowerCase().includes(query)
      );
    }
    
    // Apply date filter
    switch (filterBy) {
      case 'today':
        filtered = filtered.filter(event => isSameDay(new Date(event.start_time), today));
        break;
      case 'week':
        filtered = filtered.filter(event => isWithinDays(new Date(event.start_time), 7));
        break;
      case 'month':
        filtered = filtered.filter(event => isWithinDays(new Date(event.start_time), 30));
        break;
      case 'upcoming':
        filtered = filtered.filter(event => new Date(event.start_time) >= today);
        break;
    }
    
    // Apply priority filter
    if (priorityFilter !== 'all') {
      filtered = filtered.filter(event => {
        const priority = getPriorityInfo(event.priority_level);
        return priority.color === priorityFilter;
      });
    }
    
    // Sort events
    filtered.sort((a, b) => {
      let comparison = 0;
      
      switch (sortBy) {
        case 'date':
          comparison = new Date(a.start_time).getTime() - new Date(b.start_time).getTime();
          break;
        case 'priority':
          comparison = (b.priority_level || 1) - (a.priority_level || 1);
          break;
        case 'title':
          comparison = a.title.localeCompare(b.title);
          break;
        case 'duration':
          const durationA = new Date(a.end_time).getTime() - new Date(a.start_time).getTime();
          const durationB = new Date(b.end_time).getTime() - new Date(b.start_time).getTime();
          comparison = durationA - durationB;
          break;
      }
      
      return sortAscending ? comparison : -comparison;
    });
    
    return filtered;
  }, [events, searchQuery, sortBy, filterBy, priorityFilter, sortAscending, today]);
  
  // Group events by date for better organization
  const eventsByDate = useMemo(() => {
    const groups: { [key: string]: Event[] } = {};
    
    filteredAndSortedEvents.forEach(event => {
      const dateKey = new Date(event.start_time).toDateString();
      if (!groups[dateKey]) {
        groups[dateKey] = [];
      }
      groups[dateKey].push(event);
    });
    
    return Object.entries(groups).sort(([a], [b]) => 
      new Date(a).getTime() - new Date(b).getTime()
    );
  }, [filteredAndSortedEvents]);
  
  const handleEventClick = useCallback((event: Event) => {
    if (expandedEvent === event.id) {
      setExpandedEvent(null);
    } else {
      setExpandedEvent(event.id || null);
      if (onEventClick) {
        onEventClick(event);
      }
    }
  }, [expandedEvent, onEventClick]);
  
  const handleCreateEvent = useCallback(() => {
    if (onCreateEvent) {
      onCreateEvent(new Date());
    }
  }, [onCreateEvent]);
  
  const clearFilters = useCallback(() => {
    setSearchQuery('');
    setFilterBy('upcoming');
    setPriorityFilter('all');
    setSortBy('date');
    setSortAscending(true);
  }, []);
  
  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header with Search and Controls */}
      <div className="flex-shrink-0 border-b border-gray-200 p-6">
        <div className="flex flex-col space-y-4">
          {/* Title and Stats */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Schedule</h2>
              <p className="text-sm text-gray-600">
                {filteredAndSortedEvents.length} event{filteredAndSortedEvents.length !== 1 ? 's' : ''} found
              </p>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={handleCreateEvent}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
              >
                + New Event
              </button>
              
              <button
                onClick={() => setShowFilters(!showFilters)}
                title="Toggle filters"
                className={`
                  p-2 rounded-md transition-colors
                  ${showFilters ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}
                `}
              >
                <AdjustmentsHorizontalIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
          
          {/* Search Bar */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search events by title, description, or location..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          {/* Filters Panel */}
          <AnimatePresence>
            {showFilters && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="bg-gray-50 rounded-lg p-4 border border-gray-200"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {/* Sort Options */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Sort by</label>
                    <select
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value as SortOption)}
                      aria-label="Sort events by"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                    >
                      {SORT_OPTIONS.map(option => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                    <button
                      onClick={() => setSortAscending(!sortAscending)}
                      className="mt-1 text-xs text-blue-600 hover:text-blue-800 flex items-center"
                    >
                      {sortAscending ? <ChevronUpIcon className="h-3 w-3" /> : <ChevronDownIcon className="h-3 w-3" />}
                      {sortAscending ? 'Ascending' : 'Descending'}
                    </button>
                  </div>
                  
                  {/* Date Filter */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Time Range</label>
                    <select
                      value={filterBy}
                      onChange={(e) => setFilterBy(e.target.value as FilterOption)}
                      aria-label="Filter events by time range"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                    >
                      {FILTER_OPTIONS.map(option => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  {/* Priority Filter */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                    <select
                      value={priorityFilter}
                      onChange={(e) => setPriorityFilter(e.target.value as PriorityFilter)}
                      aria-label="Filter events by priority level"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                    >
                      {PRIORITY_FILTERS.map(option => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  {/* Clear Filters */}
                  <div className="flex items-end">
                    <button
                      onClick={clearFilters}
                      className="w-full px-3 py-2 text-sm bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
                    >
                      Clear Filters
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
      
      {/* Events List */}
      <div className="flex-1 overflow-y-auto">
        {eventsByDate.length === 0 ? (
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="text-center text-gray-500">
              <CalendarIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <h3 className="text-lg font-medium mb-2">No events found</h3>
              <p className="text-sm">
                {searchQuery ? 'Try adjusting your search or filters.' : 'Create your first event to get started.'}
              </p>
              {!searchQuery && (
                <button
                  onClick={handleCreateEvent}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  Create Event
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="p-6 space-y-6">
            {eventsByDate.map(([dateStr, dayEvents]) => {
              const date = new Date(dateStr);
              const isToday = isSameDay(date, today);
              
              return (
                <div key={dateStr} className="space-y-4">
                  {/* Date Header */}
                  <div className={`
                    sticky top-0 z-10 bg-white border-b border-gray-200 pb-2 mb-4
                    ${isToday ? 'border-blue-300' : ''}
                  `}>
                    <div className="flex items-center space-x-3">
                      <h3 className={`
                        text-lg font-semibold
                        ${isToday ? 'text-blue-600' : 'text-gray-900'}
                      `}>
                        {formatEventDate(date)}
                      </h3>
                      <span className="text-sm text-gray-500">
                        {date.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
                      </span>
                      <div className="flex-1" />
                      <span className="text-xs text-gray-400">
                        {dayEvents.length} event{dayEvents.length !== 1 ? 's' : ''}
                      </span>
                    </div>
                  </div>
                  
                  {/* Events for this date */}
                  <div className="space-y-3">
                    {dayEvents.map((event) => {
                      const startTime = new Date(event.start_time);
                      const endTime = new Date(event.end_time);
                      const priority = getPriorityInfo(event.priority_level);
                      const isExpanded = expandedEvent === event.id;
                      const duration = getDuration(startTime, endTime);
                      
                      return (
                        <motion.div
                          key={event.id}
                          layout
                          className={`
                            border-l-4 bg-white rounded-lg shadow-sm border border-gray-200
                            cursor-pointer hover:shadow-md transition-all duration-200
                            ${priority.bgColor} border-l-${priority.color}-400
                          `}
                          onClick={() => handleEventClick(event)}
                          whileHover={{ x: 4 }}
                        >
                          <div className="p-4">
                            {/* Event Header */}
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <div className="flex items-center space-x-3 mb-2">
                                  <h4 className={`font-semibold ${priority.textColor}`}>
                                    {event.title}
                                  </h4>
                                  <span className={`
                                    px-2 py-1 text-xs rounded-full
                                    bg-${priority.color}-100 text-${priority.color}-700
                                  `}>
                                    {priority.label}
                                  </span>
                                </div>
                                
                                <div className="flex items-center space-x-4 text-sm text-gray-600">
                                  <div className="flex items-center space-x-1">
                                    <ClockIcon className="h-4 w-4" />
                                    <span>{formatEventTime(startTime, endTime)}</span>
                                    <span className="text-xs text-gray-400">({duration})</span>
                                  </div>
                                  
                                  {event.location && (
                                    <div className="flex items-center space-x-1">
                                      <MapPinIcon className="h-4 w-4" />
                                      <span className="truncate max-w-48">{event.location}</span>
                                    </div>
                                  )}
                                </div>
                              </div>
                              
                              <div className="flex items-center space-x-2">
                                {event.priority_confidence && (
                                  <span className="text-xs text-gray-500">
                                    {Math.round(event.priority_confidence * 100)}%
                                  </span>
                                )}
                                <motion.div
                                  animate={{ rotate: isExpanded ? 180 : 0 }}
                                  transition={{ duration: 0.2 }}
                                >
                                  <ChevronDownIcon className="h-5 w-5 text-gray-400" />
                                </motion.div>
                              </div>
                            </div>
                            
                            {/* Expanded Details */}
                            <AnimatePresence>
                              {isExpanded && (
                                <motion.div
                                  initial={{ opacity: 0, height: 0 }}
                                  animate={{ opacity: 1, height: 'auto' }}
                                  exit={{ opacity: 0, height: 0 }}
                                  className="mt-4 pt-4 border-t border-gray-200"
                                >
                                  <div className="space-y-3">
                                    {event.description && (
                                      <div className="flex items-start space-x-2">
                                        <DocumentTextIcon className="h-4 w-4 text-gray-400 mt-0.5" />
                                        <div>
                                          <p className="text-sm text-gray-700 leading-relaxed">
                                            {event.description}
                                          </p>
                                        </div>
                                      </div>
                                    )}
                                    
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                                      {event.created_via && (
                                        <div className="flex items-center space-x-2">
                                          <UserIcon className="h-4 w-4 text-gray-400" />
                                          <span className="text-gray-600">
                                            Created via: <span className="font-medium capitalize">{event.created_via}</span>
                                          </span>
                                        </div>
                                      )}
                                      
                                      <div className="flex items-center space-x-2">
                                        <CalendarDaysIcon className="h-4 w-4 text-gray-400" />
                                        <span className="text-gray-600">
                                          Created: {event.created_at ? new Date(event.created_at).toLocaleDateString() : 'Unknown'}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                </motion.div>
                              )}
                            </AnimatePresence>
                          </div>
                        </motion.div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default ScheduleView;
