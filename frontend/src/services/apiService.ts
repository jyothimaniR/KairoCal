/**
 * API Service for KairoCal Backend Integration
 * Handles all backend API calls for events, analytics, and BERT features
 */

import { API_V1 } from '../config/api';

export interface Event {
  id?: string;
  title: string;
  description?: string;
  start_time: string; // ISO date string
  end_time: string; // ISO date string
  // Date-only (no specific time). When true, treat as scheduled for the day without time.
  all_day?: boolean;
  // Backend currently uses is_all_day; keep both for compatibility
  is_all_day?: boolean;
  location?: string;
  priority_level?: number; // 1-5 scale
  priority_confidence?: number;
  classification_method?: string;
  meeting_outcome?: string;
  effectiveness_rating?: number;
  energy_level?: number;
  created_via?: string;
  user_id?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ProductivityMetrics {
  currentScore: number;
  weeklyChange: number;
  peakHours: string[];
  conflictsResolved: number;
  voiceEvents: number;
  meetingEfficiency: number;
  focusScore: number;
}

export interface PriorityAlert {
  id: string;
  original_priority: number;
  suggested_priority: number;
  confidence: number;
  reasoning: string;
  keywords: string[];
  event_title: string;
  timestamp: string;
}

export interface VoiceHealth {
  status: 'healthy' | 'unavailable' | 'error';
  services?: Record<string, string>;
}

export interface AnalyticsHealth {
  status: 'healthy' | 'unavailable' | 'error';
  details?: Record<string, unknown>;
}

export interface SystemHealthSummary {
  voice: VoiceHealth;
  analytics: AnalyticsHealth;
  // Back-compat: some components expect `bert`
  bert?: AnalyticsHealth;
}

class APIService {
  // Feature flag (runtime overrideable) for using server conflicts instead of client heuristic
  conflictsServerEnabled = true; // toggle off to revert to client-side only
  // Shadow compare window (ms). After this time we can stop logging drift.
  conflictsShadowUntil = Date.now() + 24 * 60 * 60 * 1000; // 1 day

  setConflictsServerEnabled(on: boolean) {
    this.conflictsServerEnabled = on;
  }

  // --- Conflicts API (server) ---
  async conflictsCheck(
    payload: {
      title: string;
      start_time: string;
      end_time: string;
      description?: string;
      location?: string;
      is_all_day?: boolean;
    },
    userId: string = 'frontend-test-user'
  ): Promise<any | null> {
    try {
      const res = await fetch(`${API_V1}/conflicts/check?cognito_sub=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        console.warn('conflictsCheck failed', res.status, await res.text());
        return null;
      }
      return await res.json();
    } catch (e) {
      console.error('conflictsCheck error', e);
      return null;
    }
  }

  async conflictsResolve(
    payload: {
      title: string;
      start_time: string;
      end_time: string;
      description?: string;
      location?: string;
      is_all_day?: boolean;
      max_alternatives?: number;
      auto_resolve?: boolean;
    },
    userId: string = 'frontend-test-user'
  ): Promise<any | null> {
    try {
      const res = await fetch(`${API_V1}/conflicts/resolve?cognito_sub=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        console.warn('conflictsResolve failed', res.status, await res.text());
        return null;
      }
      return await res.json();
    } catch (e) {
      console.error('conflictsResolve error', e);
      return null;
    }
  }

  async smartReschedule(
    eventId: string,
    opts: { preferred_date?: string; max_alternatives?: number } = {},
    userId: string = 'frontend-test-user'
  ): Promise<any | null> {
    try {
      if (!eventId) return null;
      const params = new URLSearchParams({ cognito_sub: userId });
      if (opts.preferred_date) params.append('preferred_date', opts.preferred_date);
      if (opts.max_alternatives) params.append('max_alternatives', String(opts.max_alternatives));
      const res = await fetch(`${API_V1}/conflicts/smart-reschedule/${eventId}?${params.toString()}`, {
        method: 'POST',
      });
      if (!res.ok) {
        console.warn('smartReschedule failed', res.status, await res.text());
        return null;
      }
      return await res.json();
    } catch (e) {
      console.error('smartReschedule error', e);
      return null;
    }
  }
  // Get user events with optional filtering
  async getEvents(
    userId: string = 'frontend-test-user',
    filters: Record<string, string> = {}
  ): Promise<Event[]> {
    try {
      const params = new URLSearchParams({
        cognito_sub: userId,
        ...filters,
      });
      const response = await fetch(`${API_V1}/events?${params}`);
      if (!response.ok) throw new Error(`Failed to fetch events: ${response.statusText}`);
      const raw = await response.json();
      // Normalize all_day vs is_all_day
      return (raw || []).map((e: any) => ({
        ...e,
        all_day: e.all_day ?? e.is_all_day ?? false,
        is_all_day: e.is_all_day ?? e.all_day ?? false,
      }));
    } catch (error) {
      console.error('Error fetching events:', error);
      return [];
    }
  }

  // Get high-priority events
  async getHighPriorityEvents(userId: string = 'frontend-test-user'): Promise<Event[]> {
    try {
      const response = await fetch(
        `${API_V1}/events/priority/high-priority?cognito_sub=${userId}&max_priority=2`
      );
      if (!response.ok) throw new Error(`Failed to fetch high-priority events: ${response.statusText}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching high-priority events:', error);
      return [];
    }
  }

  // Get today's events
  async getTodaysEvents(userId: string = 'frontend-test-user'): Promise<Event[]> {
    try {
      const todayDate = new Date();
      const startIso = new Date(
        Date.UTC(
          todayDate.getUTCFullYear(),
          todayDate.getUTCMonth(),
          todayDate.getUTCDate(),
          0,
          0,
          0
        )
      ).toISOString();
      const endDay = new Date(todayDate.getTime() + 24 * 60 * 60 * 1000);
      const endIso = new Date(
        Date.UTC(endDay.getUTCFullYear(), endDay.getUTCMonth(), endDay.getUTCDate(), 0, 0, 0)
      ).toISOString();

      return await this.getEvents(userId, { start_date: startIso, end_date: endIso });
    } catch (error) {
      console.error("Error fetching today's events:", error);
      return [];
    }
  }

  // Get productivity analytics from backend
  async getProductivityMetrics(userId: string = 'frontend-test-user'):
    Promise<ProductivityMetrics> {
    try {
      const response = await fetch(
        `${API_V1}/analytics/productivity/metrics?cognito_sub=${userId}`
      );
      if (!response.ok) {
        // Fallback mock if endpoint not available
        return {
          currentScore: 87,
          weeklyChange: 5,
          peakHours: ['9:00-11:00 AM'],
          conflictsResolved: 3,
          voiceEvents: 12,
          meetingEfficiency: 85,
          focusScore: 90,
        };
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching productivity metrics:', error);
      return {
        currentScore: 87,
        weeklyChange: 5,
        peakHours: ['9:00-11:00 AM'],
        conflictsResolved: 3,
        voiceEvents: 12,
        meetingEfficiency: 85,
        focusScore: 90,
      };
    }
  }

  // Get priority trend analytics
  async getPriorityTrends(userId: string = 'frontend-test-user'): Promise<Record<string, unknown>> {
    try {
      const response = await fetch(
        `${API_V1}/analytics/priority/trends?cognito_sub=${userId}`
      );
      if (!response.ok) throw new Error(`Failed to fetch priority trends: ${response.statusText}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching priority trends:', error);
      throw error;
    }
  }

  // Get BERT performance analytics
  async getBertPerformance(userId: string = 'frontend-test-user'): Promise<Record<string, unknown>> {
    try {
      const response = await fetch(
        `${API_V1}/analytics/bert/performance?cognito_sub=${userId}`
      );
      if (!response.ok) throw new Error(`Failed to fetch BERT performance: ${response.statusText}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching BERT performance:', error);
      throw error;
    }
  }

  // Compute metrics client-side from events and analytics
  async getComputedProductivityMetrics(userId: string = 'frontend-test-user'):
    Promise<ProductivityMetrics> {
    try {
      const [events, priorityTrends, bertPerformance] = await Promise.all([
        this.getEvents(userId),
        this.getPriorityTrends(userId),
        this.getBertPerformance(userId),
      ]);

      const voiceEvents = events.filter((e) => e.created_via === 'voice').length;
      const highPriorityEvents = events.filter((e) => (e.priority_level || 3) <= 2).length;

      const currentScore = Math.min(87 + voiceEvents * 2 + highPriorityEvents * 3, 100);

      const recentEvents = events.filter((e) => {
        if (e.created_at) {
          const eventDate = new Date(e.created_at);
          const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
          return eventDate >= weekAgo;
        }
        return false;
      });
      const weeklyChange = Math.min(recentEvents.length, 15);

  const insights = (priorityTrends?.['insights'] as Record<string, unknown> | undefined);
  const overview = (bertPerformance?.['classification_overview'] as Record<string, unknown> | undefined);
      const totalAnalyzed = (insights?.['total_events_analyzed'] as number) || 0;
      const adoptionRate = (overview?.['bert_adoption_rate'] as number) || 0;

      return {
        currentScore,
        weeklyChange,
        peakHours: ['9:00-11:00 AM'],
        conflictsResolved: totalAnalyzed,
        voiceEvents,
        meetingEfficiency: Math.round(adoptionRate * 100),
        focusScore: Math.round(currentScore * 0.9),
      };
    } catch (error) {
      console.error('Error computing productivity metrics:', error);
      return {
        currentScore: 87,
        weeklyChange: 5,
        peakHours: ['9:00-11:00 AM'],
        conflictsResolved: 3,
        voiceEvents: 2,
        meetingEfficiency: 85,
        focusScore: 78,
      };
    }
  }

  async getPriorityAnalytics(userId: string = 'frontend-test-user'): Promise<Record<string, unknown> | null> {
    try {
      const response = await fetch(
        `${API_V1}/analytics/priority/trends?cognito_sub=${userId}`
      );
      if (!response.ok)
        throw new Error(`Failed to fetch priority analytics: ${response.statusText}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching priority analytics:', error);
      return null;
    }
  }

  /**
   * Create an event from voice input using the proper voice API
   */
  async createVoiceEvent(
    voiceText: string,
    userId: string = 'frontend-test-user'
  ): Promise<{ success: boolean; event_id?: string; event_data: Record<string, unknown>; message?: string }> {
    console.log('🎤 Creating voice event:', { voiceText, userId });
    console.log('🌐 API URL:', `${API_V1}/voice/create-event`);

    // Get user's duration preference from settings
    let durationPreference: string | number = 'smart';
    try {
      const userSettings = localStorage.getItem('user-preferences');
      if (userSettings) {
        const parsed = JSON.parse(userSettings);
        durationPreference = parsed.default_event_duration || 'smart';
      }
    } catch (error) {
      console.log('📝 Using default duration preference (smart)');
    }

    console.log('⏱️ Duration preference:', durationPreference);

    try {
      const response = await fetch(`${API_V1}/voice/create-event`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          voice_text: voiceText,
          user_id: userId,
          auto_schedule: true,
          duration_preference: durationPreference
        }),
      });

      console.log('📡 Response status:', response.status);
      console.log('📡 Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ API Error Response:', errorText);
        throw new Error(`Voice event creation failed: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Voice event created:', data);
      
      return {
        success: data.success || false,
        event_id: data.event_id,
        event_data: data.event_data || {},
        message: data.message || 'Event created successfully'
      };
    } catch (error) {
      console.error('❌ Voice event creation failed:', error);
      throw error;
    }
  }

  // Create event
  async createEvent(
    eventData: Partial<Event>,
    userId: string = 'frontend-test-user'
  ): Promise<Event | null> {
    try {
      // Helper function to safely format datetime without timezone conversion
      const safeFormatDateTime = (dateTimeInput: string | undefined): string => {
        if (!dateTimeInput) {
          // Default fallback - current time formatted without timezone conversion
          const now = new Date();
          const year = now.getFullYear();
          const month = String(now.getMonth() + 1).padStart(2, '0');
          const day = String(now.getDate()).padStart(2, '0');
          const hours = String(now.getHours()).padStart(2, '0');
          const minutes = String(now.getMinutes()).padStart(2, '0');
          const seconds = String(now.getSeconds()).padStart(2, '0');
          return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
        }
        
        // If already properly formatted (YYYY-MM-DDTHH:mm:ss), pass through
        if (typeof dateTimeInput === 'string' && dateTimeInput.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/)) {
          return dateTimeInput;
        }
        
        // If ISO string or other format, parse and reformat without timezone conversion
        const date = new Date(dateTimeInput);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
      };
      
      const payload = {
        ...eventData,
        start_time: safeFormatDateTime(eventData.start_time),
        end_time: safeFormatDateTime(eventData.end_time) || (() => {
          // Default end time: 1 hour after start time
          const startTime = safeFormatDateTime(eventData.start_time);
          const startDate = new Date(startTime);
          startDate.setHours(startDate.getHours() + 1);
          return safeFormatDateTime(startDate.toISOString());
        })(),
  // Mark typed-created events as manual so UI does not show voice tag
  created_via: eventData.created_via ?? 'manual',
        classification_method: 'auto',
      };
      const response = await fetch(
        `${API_V1}/events?cognito_sub=${userId}&auto_classify_priority=true`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }
      );
      if (!response.ok) throw new Error(`Failed to create event: ${response.statusText}`);
      return await response.json();
    } catch (error) {
      console.error('Error creating event:', error);
      return null;
    }
  }

  // Update event priority
  async updateEventPriority(
    eventId: string,
    priority: number,
    userId: string = 'frontend-test-user'
  ): Promise<boolean> {
    try {
      if (!eventId || eventId.length < 32) return false;
      const url = `${API_V1}/events/${eventId}?cognito_sub=${userId}`;
      const response = await fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priority_level: priority }),
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Failed to update event priority: ${response.statusText} - ${errorText}`
        );
      }
      await response.json();
      return true;
    } catch (error) {
      console.error('Error updating event priority:', error);
      return false;
    }
  }

  // Reschedule event
  async rescheduleEvent(
    eventId: string,
    newStartTime: string,
    newEndTime: string,
    userId: string = 'frontend-test-user'
  ): Promise<boolean> {
    try {
      if (!eventId || eventId.length < 32) return false;
      
      // TIMEZONE FIX: Ensure we're sending local time format, not UTC
      // If input is a Date object (from drag-drop), format it correctly
      const formatLocalDateTime = (timeInput: string | Date): string => {
        let date: Date;
        
        if (typeof timeInput === 'string') {
          // If already properly formatted, use as-is
          if (timeInput.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/)) {
            return timeInput;
          }
          date = new Date(timeInput);
        } else {
          date = timeInput;
        }
        
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
      };
      
      const formattedStartTime = formatLocalDateTime(newStartTime);
      const formattedEndTime = formatLocalDateTime(newEndTime);
      
      console.log(`🔧 RESCHEDULE API - Formatted times: ${formattedStartTime} to ${formattedEndTime}`);
      
      const response = await fetch(`${API_V1}/events/${eventId}?cognito_sub=${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          start_time: formattedStartTime, 
          end_time: formattedEndTime 
        }),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Failed to reschedule event: ${response.statusText} - ${errorText}`
        );
      }
      await response.json();
      return true;
    } catch (error) {
      console.error('Error rescheduling event:', error);
      return false;
    }
  }

  // Update event (comprehensive)
  async updateEvent(eventId: string, eventData: Partial<Event>, userId: string = 'frontend-test-user'): Promise<Event | null> {
    try {
      if (!eventId || eventId.length < 32) return null;
      
      const response = await fetch(`${API_V1}/events/${eventId}?cognito_sub=${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(eventData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Failed to update event: ${response.statusText} - ${errorText}`
        );
      }
      
      const updatedEvent = await response.json();
      return updatedEvent;
    } catch (error) {
      console.error('Error updating event:', error);
      return null;
    }
  }

  // Delete event
  async deleteEvent(eventId: string, userId: string = 'frontend-test-user'): Promise<boolean> {
    try {
      if (!eventId || eventId.length < 32) return false;
      const response = await fetch(`${API_V1}/events/${eventId}?cognito_sub=${userId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to delete event: ${response.statusText} - ${errorText}`);
      }
      await response.json();
      return true;
    } catch (error) {
      console.error('Error deleting event:', error);
      return false;
    }
  }

  // Get priority alerts
  async getPriorityAlerts(userId: string = 'frontend-test-user'): Promise<PriorityAlert[]> {
    try {
      // Simple client-side heuristic: propose upgrades for medium/low priority upcoming events with keywords
      const events = await this.getEvents(userId);
      const now = Date.now();
      const alerts: PriorityAlert[] = [];
      const keywordBoost = [/ceo/i, /interview/i, /deadline/i, /doctor|dentist/i, /review/i];

      for (const e of events) {
        if (!e.start_time) continue;
        const t = new Date(e.start_time).getTime();
        if (t < now) continue; // future only
        const original = e.priority_level ?? 3;
        let suggested = original;
        const text = `${e.title} ${e.description || ''}`;
        if (original > 2 && keywordBoost.some(rx => rx.test(text))) {
          suggested = Math.max(1, original - 1);
        }
        if (suggested < original) {
          alerts.push({
            id: `alert-${e.id}`,
            original_priority: original,
            suggested_priority: suggested,
            confidence: 0.75,
            reasoning: 'Keyword-based priority boost suggested by client heuristic',
            keywords: keywordBoost.filter(rx => rx.test(text)).map(rx => rx.source),
            event_title: e.title,
            timestamp: new Date().toISOString()
          });
        }
      }
      return alerts;
    } catch (error) {
      console.error('Error building priority alerts:', error);
      return [];
    }
  }

  // System health
  async getSystemHealth(): Promise<SystemHealthSummary> {
    try {
      const [voiceRes, analyticsRes] = await Promise.all([
        fetch(`${API_V1}/voice/health`),
        fetch(`${API_V1}/analytics/health`)
      ]);
      const voice: VoiceHealth = voiceRes.ok
        ? await voiceRes.json()
        : { status: 'unavailable' };
      const analytics: AnalyticsHealth = analyticsRes.ok
        ? await analyticsRes.json()
        : { status: 'unavailable' };
  // Back-compat alias for components referencing `bert`
  return { voice, analytics, bert: analytics };
    } catch (error) {
      console.error('Error fetching system health:', error);
      return { voice: { status: 'error' }, analytics: { status: 'error' } } as SystemHealthSummary;
    }
  }

  // ======================================
  // NEW: PRIORITY-BASED SCHEDULING METHODS
  // ======================================

  /**
   * Check for conflicts with a proposed event
   */
  async checkConflicts(userId: string, eventData: {
    title: string;
    start_time: string;
    end_time: string;
    description?: string;
  }): Promise<any> {
    try {
      const response = await fetch(`${API_V1}/conflicts/check?cognito_sub=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
      });

      if (!response.ok) {
        throw new Error(`Conflict check failed: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error checking conflicts:', error);
      throw error;
    }
  }

  /**
   * Get priority-based time slot suggestions
   */
  async getPriorityTimeSlots(params: {
    priority_level: number;
    duration_minutes: number;
    user_id?: string;
    preferred_date?: string;
    exclude_times?: Array<{start: string; end: string}>;
    num_suggestions?: number;
  }): Promise<{
    success: boolean;
    message: string;
    original_priority: number;
    suggested_slots: Array<{
      start_time: string;
      end_time: string;
      confidence: number;
      reasoning: string;
      priority_match_score: number;
      availability_score: number;
      is_prime_time: boolean;
      conflict_risk: number;
    }>;
    reasoning: string;
    total_slots_considered: number;
    filter_criteria_used: string[];
    fallback_used: boolean;
    processing_time_ms: number;
  }> {
    try {
      const user_id = params.user_id || 'default_user';
      const requestBody = {
        priority_level: params.priority_level,
        duration_minutes: params.duration_minutes,
        preferred_date: params.preferred_date,
        exclude_times: params.exclude_times,
        num_suggestions: params.num_suggestions || 5
      };

      const response = await fetch(`${API_V1}/priority/resolve?user_id=${user_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`Priority API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting priority time slots:', error);
      throw error;
    }
  }

  /**
   * Get priority time windows configuration
   */
  async getPriorityWindows(): Promise<{
    success: boolean;
    data: {
      priority_windows: Record<string, {name: string; hours: string; start: number; end: number}>;
      prime_business_hours: {start: number; end: number; description: string};
      extended_business_hours: {start: number; end: number; description: string};
      flexible_hours: {start: number; end: number; description: string};
      explanation: string;
    };
    message: string;
  }> {
    try {
      const response = await fetch(`${API_V1}/priority/windows`);
      
      if (!response.ok) {
        throw new Error(`Priority Windows API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting priority windows:', error);
      throw error;
    }
  }

  /**
   * Get priority system health status
   */
  async getPriorityHealth(): Promise<{
    success: boolean;
    health: {
      priority_scheduler: string;
      bert_classification: string;
      user_behavior_analytics: string;
      smart_conflict_detection: string;
      overall_status: string;
      warning?: string;
    };
    timestamp: string;
    message: string;
  }> {
    try {
      const response = await fetch(`${API_V1}/priority/health`);
      
      if (!response.ok) {
        throw new Error(`Priority Health API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting priority health:', error);
      throw error;
    }
  }

  /**
   * Test priority scheduling functionality
   */
  async testPriorityScheduling(priority: number = 3, duration: number = 60): Promise<{
    test_successful: boolean;
    priority_level: number;
    duration_minutes: number;
    suggestions_generated: number;
    reasoning: string;
    time_window_used: string;
    sample_slots: Array<{
      start: string;
      end: string;
      confidence: number;
      is_prime_time: boolean;
    }>;
    message: string;
    error?: string;
  }> {
    try {
      const response = await fetch(`${API_V1}/priority/test?priority=${priority}&duration=${duration}`);
      
      if (!response.ok) {
        throw new Error(`Priority Test API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error testing priority scheduling:', error);
      throw error;
    }
  }

  /**
   * Get base URL for direct API calls (used by components)
   */
  getBaseUrl(): string {
    return API_V1.replace('/api/v1', '');
  }
}

export const apiService = new APIService();
export default apiService;
