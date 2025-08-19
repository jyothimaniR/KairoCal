import { useState, useEffect, useCallback, useMemo } from 'react';
import { apiService } from '../services/apiService';
import type { Event, ProductivityMetrics, PriorityAlert, SystemHealthSummary } from '../services/apiService';
import { useAuth } from '../contexts/AuthContext';

export interface DashboardData {
  events: Event[];
  todaysEvents: Event[];
  highPriorityEvents: Event[];
  productivityMetrics: ProductivityMetrics;
  priorityAlerts: PriorityAlert[];
  systemHealth: SystemHealthSummary | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: Date | null;
}

export const useDashboard = () => {
  const { user } = useAuth();
  const userId = useMemo(() => user?.uid || 'frontend-test-user', [user]);
  
  const [data, setData] = useState<DashboardData>({
    events: [],
    todaysEvents: [],
    highPriorityEvents: [],
    productivityMetrics: {
      currentScore: 0,
      weeklyChange: 0,
      peakHours: [],
      conflictsResolved: 0,
      voiceEvents: 0,
      meetingEfficiency: 0,
      focusScore: 0
    },
    priorityAlerts: [],
    systemHealth: null,
    isLoading: true,
    error: null,
    lastUpdated: null
  });

  const loadDashboardData = useCallback(async () => {
    try {
      setData(prev => ({ ...prev, isLoading: true, error: null }));

      console.log('🔄 Loading dashboard data...');

      // Load all dashboard data concurrently
      const [
        events,
        todaysEvents,
        highPriorityEvents,
        productivityMetrics,
        priorityAlerts,
        systemHealth
      ] = await Promise.all([
  apiService.getEvents(userId),
  apiService.getTodaysEvents(userId),
  apiService.getHighPriorityEvents(userId),
  apiService.getComputedProductivityMetrics(userId),
  apiService.getPriorityAlerts(userId),
        apiService.getSystemHealth()
      ]);

      console.log('✅ Dashboard data loaded:', {
        eventsCount: events.length,
        todaysEventsCount: todaysEvents.length,
        highPriorityCount: highPriorityEvents.length,
        priorityAlertsCount: priorityAlerts.length
      });

      setData(prev => ({
        ...prev,
        events,
        todaysEvents,
        highPriorityEvents,
        productivityMetrics,
        priorityAlerts,
        systemHealth,
        isLoading: false,
        lastUpdated: new Date()
      }));

    } catch (error) {
      console.error('❌ Error loading dashboard data:', error);
      setData(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load dashboard data'
      }));
    }
  }, [userId]);

  // Load data on mount and when userId changes
  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  // Auto-refresh every 5 minutes
  useEffect(() => {
    const interval = setInterval(() => {
      console.log('🔄 Auto-refreshing dashboard data...');
      loadDashboardData();
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(interval);
  }, [loadDashboardData]);

  const createEvent = useCallback(async (eventData: Partial<Event>) => {
    try {
      console.log('🆕 Creating new event:', eventData);
      const newEvent = await apiService.createEvent(eventData);
      
      if (newEvent) {
        // Refresh dashboard data to include the new event
        await loadDashboardData();
        console.log('✅ Event created and dashboard refreshed');
        return newEvent;
      }
      
      throw new Error('Failed to create event');
    } catch (error) {
      console.error('❌ Error creating event:', error);
      setData(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to create event'
      }));
      return null;
    }
  }, [loadDashboardData]);

  const updateEventPriority = useCallback(async (eventId: string, priority: number) => {
    try {
      console.log(`🔄 Updating event ${eventId} priority to ${priority}`);
      
      // Clear any previous errors
      setData(prev => ({ ...prev, error: null }));
      
      const success = await apiService.updateEventPriority(eventId, priority);
      
      if (success) {
        // Refresh dashboard data to reflect the priority change
        await loadDashboardData();
        console.log('✅ Event priority updated and dashboard refreshed');
        return true;
      } else {
        const errorMsg = 'Failed to update event priority - API returned false';
        console.error('❌', errorMsg);
        setData(prev => ({ ...prev, error: errorMsg }));
        return false;
      }
      
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : 'Failed to update event priority';
      console.error('❌ Error updating event priority:', error);
      setData(prev => ({
        ...prev,
        error: `Failed to update event priority: ${errorMsg}`
      }));
      return false;
    }
  }, [loadDashboardData]);

  const dismissPriorityAlert = useCallback((alertId: string) => {
    setData(prev => ({
      ...prev,
      priorityAlerts: prev.priorityAlerts.filter(alert => alert.id !== alertId)
    }));
  }, []);

  const clearError = useCallback(() => {
    setData(prev => ({ ...prev, error: null }));
  }, []);

  // Helper functions for common data transformations
  const getEventsByPriority = useCallback((priority: number) => {
    return data.events.filter(event => event.priority_level === priority);
  }, [data.events]);

  const getEventsCreatedViaVoice = useCallback(() => {
    return data.events.filter(event => event.created_via === 'voice');
  }, [data.events]);

  const getUpcomingEvents = useCallback((hours: number = 24) => {
    const cutoff = new Date(Date.now() + hours * 60 * 60 * 1000);
    return data.events.filter(event => {
      const eventTime = new Date(event.start_time);
      return eventTime > new Date() && eventTime <= cutoff;
    });
  }, [data.events]);

  return {
    ...data,
    loadDashboardData,
    createEvent,
    updateEventPriority,
    dismissPriorityAlert,
    clearError,
    // Helper functions
    getEventsByPriority,
    getEventsCreatedViaVoice,
    getUpcomingEvents
  };
};

export default useDashboard;
