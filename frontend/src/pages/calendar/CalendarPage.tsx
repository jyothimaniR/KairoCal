import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CalendarIcon } from '@heroicons/react/24/outline';
import type { Event } from '../../services/apiService';
import { apiService } from '../../services/apiService';
import DayView from './views/DayView';
import WeekView from './views/WeekView';
import MonthView from './views/MonthView';
import ScheduleView from './views/ScheduleView';
import YearView from './views/YearView';
import ViewSelector from './components/ViewSelector';
import DateNavigation from './components/DateNavigation';
import EventModal from './components/EventModal';

type ViewType = 'day' | 'week' | 'month' | 'schedule' | 'year';

const CalendarPage: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewType>('week');
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [isEventModalOpen, setIsEventModalOpen] = useState(false);
  const [createEventDate, setCreateEventDate] = useState<Date | null>(null);

  // Load events from API
  const loadEvents = async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('🔄 Loading calendar events...');
      
      const eventsData = await apiService.getEvents();
      console.log('✅ Calendar events loaded:', eventsData.length);
      
      setEvents(eventsData);
    } catch (err) {
      console.error('❌ Error loading events:', err);
      setError(err instanceof Error ? err.message : 'Failed to load events');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const handleDateChange = (date: Date) => {
    setCurrentDate(date);
  };

  const handleEventClick = (event: Event) => {
    setSelectedEvent(event);
    setIsEventModalOpen(true);
  };

  const handleCreateEvent = (date: Date) => {
    setCreateEventDate(date);
    setSelectedEvent(null);
    setIsEventModalOpen(true);
  };

  const handleEventSave = async (eventData: Partial<Event>): Promise<boolean> => {
    try {
      if (selectedEvent?.id) {
        // Update existing event
        await apiService.updateEvent(selectedEvent.id, eventData);
      } else {
        // Create new event
        await apiService.createEvent(eventData);
      }
      
      // Refresh events list
      await loadEvents();
      return true;
    } catch (error) {
      console.error('Error saving event:', error);
      return false;
    }
  };

  const handleEventDelete = async (eventId: string): Promise<boolean> => {
    try {
      await apiService.deleteEvent(eventId);
      await loadEvents();
      return true;
    } catch (error) {
      console.error('Error deleting event:', error);
      return false;
    }
  };

  const handleEventUpdate = () => {
    // Refresh events after any update
    loadEvents();
  };

  const handleEventModalClose = () => {
    setIsEventModalOpen(false);
    setSelectedEvent(null);
    setCreateEventDate(null);
  };

  const renderCurrentView = () => {
    const commonProps = {
      events,
      selectedDate: currentDate,
      onSelectDate: setCurrentDate,
      onEventClick: handleEventClick,
      onCreateEvent: handleCreateEvent,
      onEventUpdate: handleEventUpdate,
      currentDate,
      onDateChange: handleDateChange,
    };

    switch (currentView) {
      case 'day':
        return <DayView {...commonProps} />;
      case 'week':
        return <WeekView {...commonProps} />;
      case 'month':
        return <MonthView {...commonProps} />;
      case 'schedule':
        return <ScheduleView {...commonProps} />;
      case 'year':
        return <YearView {...commonProps} />;
      default:
        return <WeekView {...commonProps} />;
    }
  };

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CalendarIcon className="h-5 w-5 text-red-400" aria-hidden="true" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Calendar Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
              <div className="mt-4">
                <button
                  onClick={loadEvents}
                  className="bg-red-100 px-2 py-1 text-xs font-medium text-red-800 rounded hover:bg-red-200"
                >
                  Retry
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-full bg-gray-50"
    >
      {/* Calendar Header */}
      <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-semibold text-gray-900 flex items-center">
              <CalendarIcon className="h-6 w-6 mr-2 text-purple-600" />
              Calendar
            </h1>
            
            {/* Date Navigation */}
            <DateNavigation
              currentDate={currentDate}
              onDateChange={handleDateChange}
              currentView={currentView}
              onToday={() => setCurrentDate(new Date())}
            />
          </div>

          <div className="flex items-center space-x-4">
            {/* Loading indicator */}
            {isLoading && (
              <div className="text-sm text-gray-500">
                Loading events...
              </div>
            )}

            {/* View Selector */}
            <ViewSelector
              currentView={currentView}
              onViewChange={setCurrentView}
            />

            {/* Refresh Button */}
            <button
              onClick={loadEvents}
              disabled={isLoading}
              className="px-3 py-1.5 text-sm bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
            >
              Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Calendar Content */}
      <div className="flex-1 overflow-hidden">
        {renderCurrentView()}
      </div>

      {/* Event Modal */}
      {isEventModalOpen && (
        <EventModal
          event={selectedEvent}
          initialDate={createEventDate || undefined}
          isOpen={isEventModalOpen}
          onClose={handleEventModalClose}
          onSave={handleEventSave}
          onDelete={handleEventDelete}
        />
      )}
    </motion.div>
  );
};

export default CalendarPage;
