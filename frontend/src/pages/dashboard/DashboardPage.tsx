import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  ExclamationTriangleIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import { getPriorityInfo } from '../../utils/priorityUtils';
import { getEventIcon } from '../../utils/eventIconUtils';
import UnifiedEventCreator from '../../components/voice/UnifiedEventCreator';
import MiniCalendar from '../../components/calendar/MiniCalendar';
import AnalyticsPanel from '../../components/analytics/AnalyticsPanel';
import { RecentActivity } from '../../components/dashboard/RecentActivity';
import PriorityConflictResolver from '../../components/conflicts/PriorityConflictResolver';
import { PriorityChangeModal } from '../../components/modals/PriorityChangeModal';
import { useDashboard } from '../../hooks/useDashboard';
import { useSystemHealth } from '../../hooks/useSystemHealth';

const DashboardPage: React.FC = () => {
  const {
    events,
    productivityMetrics,
    isLoading,
    error,
    lastUpdated,
    loadDashboardData,
    updateEventPriority,
    clearError
  } = useDashboard();

  // Use unified system health hook for consistent BERT status
  const { systemHealth } = useSystemHealth();

  // Helper function to format priority display (imported from utils)

  // AI Priority Alerts have been permanently disabled on the dashboard.

  const handleChangePriority = (eventId: string, currentPriority: number, eventTitle: string) => {
    setPriorityModalState({
      isOpen: true,
      eventId,
      eventTitle,
      currentPriority
    });
  };

  const handlePriorityModalClose = () => {
    setPriorityModalState({
      isOpen: false,
      eventId: null,
      eventTitle: '',
      currentPriority: 3
    });
  };

  const handlePriorityModalSave = async (newPriority: number): Promise<boolean> => {
    if (!priorityModalState.eventId) return false;
    
    try {
      const success = await updateEventPriority(priorityModalState.eventId, newPriority);
      if (success) {
        // Refresh the data to show updated priority
        await loadDashboardData();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error updating priority:', error);
      return false;
    }
  };

  // Calendar selection state
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());

  const isSameDay = (a: Date, b: Date) =>
    a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

  const dayEvents = useMemo(() => {
    return (events || []).filter(e => {
      const d = new Date(e.start_time);
      return isSameDay(d, selectedDate);
    }).sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime());
  }, [events, selectedDate]);

  const [showAllDayEvents, setShowAllDayEvents] = useState(false);

  // Priority change modal state
  const [priorityModalState, setPriorityModalState] = useState<{
    isOpen: boolean;
    eventId: string | null;
    eventTitle: string;
    currentPriority: number;
  }>({
    isOpen: false,
    eventId: null,
    eventTitle: '',
    currentPriority: 3
  });

  const scheduleTitle = useMemo(() => {
    const today = new Date();
    return isSameDay(selectedDate, today)
      ? "📅 Today's Schedule"
      : `📅 ${selectedDate.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}`;
  }, [selectedDate]);

  return (
    <div className="p-6 space-y-6">
      {/* Error Display */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-50 border border-red-200 rounded-xl p-4"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
              <p className="text-red-700">{error}</p>
            </div>
            <button 
              onClick={clearError}
              className="text-red-500 hover:text-red-700"
            >
              ✕
            </button>
          </div>
        </motion.div>
      )}

      {/* Loading State */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-blue-50 border border-blue-200 rounded-xl p-4"
        >
          <div className="flex items-center space-x-2">
            <ArrowPathIcon className="h-5 w-5 text-blue-500 animate-spin" />
            <p className="text-blue-700">Loading dashboard data...</p>
          </div>
        </motion.div>
      )}

  {/* AI Priority Alerts: removed by request - no alerts will render here */}

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Productivity Overview */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                📊 Productivity Overview
              </h2>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-500">
                  Updated {lastUpdated ? new Date(lastUpdated).toLocaleTimeString() : 'never'}
                </span>
                <button
                  onClick={loadDashboardData}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Refresh data"
                >
                  <ArrowPathIcon className="h-4 w-4 text-gray-500" />
                </button>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">
                  {productivityMetrics.currentScore}%
                </div>
                <div className="text-sm text-green-600 flex items-center justify-center mt-1">
                  ✅ +{productivityMetrics.weeklyChange}% this week
                </div>
                <div className="text-xs text-gray-500 mt-1">Productivity Score</div>
              </div>

              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {productivityMetrics.peakHours[0] || 'Not available'}
                </div>
                <div className="text-xs text-gray-500 mt-1">Peak Hours</div>
              </div>

              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">
                  {productivityMetrics.conflictsResolved}
                </div>
                <div className="text-xs text-gray-500 mt-1">Conflicts Resolved Today</div>
              </div>

              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">
                  {productivityMetrics.voiceEvents}
                </div>
                <div className="text-xs text-gray-500 mt-1">Voice Events Today</div>
              </div>
            </div>
          </motion.div>

          {/* Unified Event Creator - Replaces both Voice and Text inputs */}
          <div className="grid grid-cols-1 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <UnifiedEventCreator onEventCreated={loadDashboardData} />
            </motion.div>
          </div>
        </div>

        {/* Right Column - Sidebar */}
        <div className="space-y-6">
          {/* Mini Calendar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <MiniCalendar
              events={events}
              selectedDate={selectedDate}
              onSelectDate={setSelectedDate}
            />
          </motion.div>

          {/* Today's Schedule */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center justify-between">
              {scheduleTitle}
              <span className="text-sm text-gray-500">{dayEvents.length} events</span>
            </h3>
            
            <div className="space-y-3">
              {dayEvents.length === 0 ? (
                <div className="text-center py-6 text-gray-500">
                  <p>No events on this date</p>
                  <p className="text-sm mt-1">Try creating one with voice commands or Quick Add.</p>
                </div>
              ) : (
                (showAllDayEvents ? dayEvents : dayEvents.slice(0, 4)).map((event) => {
                  // PRIORITY FIX: Use getPriorityInfo instead of deprecated getPriorityLabel
                  const priorityInfo = getPriorityInfo(event.priority_level || 3);
                  const startTime = new Date(event.start_time);
                  // EMOJI FIX: Get systematic event icon instead of hardcoded emojis
                  const eventIcon = getEventIcon(event.title, (event as any).category);

                  return (
                    <div 
                      key={event.id} 
                      className={`border border-gray-200 rounded-lg p-3 mb-2 hover:shadow-md transition-shadow`}
                      title="Click priority badge to change priority level"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center font-medium text-gray-900">
                            <span className="mr-2 text-lg">{eventIcon}</span>
                            {event.title}
                          </div>
                          {(event.all_day || (event as any).is_all_day) ? (
                            <div className="text-sm text-gray-500 mt-1">All Day Event</div>
                          ) : (
                            <div className="text-sm text-gray-500 mt-1">
                              {startTime.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })} to{' '}
                              {new Date(event.end_time).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })}
                            </div>
                          )}
                          {event.location && (
                            <div className="text-xs text-gray-400 mt-1">{event.location}</div>
                          )}
                        </div>
                        <div className="text-right">
                          <div className={`text-sm font-medium mb-1 px-2 py-1 rounded-full ${priorityInfo.bgColor} ${priorityInfo.textColor} cursor-pointer hover:opacity-75`}
                               title="Click to change priority"
                               onClick={() => handleChangePriority(event.id!, event.priority_level || 3, event.title)}>
                            {priorityInfo.label} ✏️
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })
              )}

              {dayEvents.length > 4 && !showAllDayEvents && (
                <div className="text-center pt-2">
                  <button className="text-sm text-blue-600 hover:text-blue-800" onClick={() => setShowAllDayEvents(true)}>
                    View {dayEvents.length - 4} more events
                  </button>
                </div>
              )}
              {dayEvents.length > 4 && showAllDayEvents && (
                <div className="text-center pt-2">
                  <button className="text-sm text-gray-600 hover:text-gray-800" onClick={() => setShowAllDayEvents(false)}>
                    Show less
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      {/* AI Analytics Panel */}
      <AnalyticsPanel />

      {/* Smart Conflict Detection */}
      <PriorityConflictResolver />

      {/* Recent Activity */}
      <RecentActivity events={events} isLoading={isLoading} />

      {/* System Health Status */}
      {systemHealth && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl p-4 shadow-sm border border-gray-200"
        >
          <h3 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
            🔧 System Status
          </h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Voice API:</span>
              <span className={`px-2 py-1 rounded text-xs ${
                systemHealth.voice?.status === 'healthy' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {systemHealth.voice?.status === 'healthy' ? '🟢 Online' : '🔴 Offline'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">BERT AI:</span>
              <span className={`px-2 py-1 rounded text-xs ${
                systemHealth.bert?.status === 'healthy' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {systemHealth.bert?.status === 'healthy' ? '🧠 Active' : '🔴 Inactive'}
              </span>
            </div>
          </div>
        </motion.div>
      )}

      {/* Priority Change Modal */}
      <PriorityChangeModal
        isOpen={priorityModalState.isOpen}
        onClose={handlePriorityModalClose}
        currentPriority={priorityModalState.currentPriority}
        eventTitle={priorityModalState.eventTitle}
        onSave={handlePriorityModalSave}
      />
    </div>
  );
};

export default DashboardPage;
