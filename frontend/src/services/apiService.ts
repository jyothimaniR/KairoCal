/**
 * API Service for KairoCal Backend Integration
 * Handles all backend API calls for events, analytics, and BERT features
 */

import { API_V1 } from '../config/api';
import { getCurrentUserId } from '../config/user';

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

    try {
      const response = await fetch(`${API_V1}/voice/create-event`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          voice_text: voiceText,
          user_id: userId,
          auto_schedule: true
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
      const payload = {
        ...eventData,
        start_time: eventData.start_time
          ? new Date(eventData.start_time).toISOString()
          : new Date().toISOString(),
        end_time: eventData.end_time
          ? new Date(eventData.end_time).toISOString()
          : new Date(Date.now() + 60 * 60 * 1000).toISOString(),
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
      const response = await fetch(`${API_V1}/events/${eventId}?cognito_sub=${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_time: newStartTime, end_time: newEndTime }),
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
}

export const apiService = new APIService();
export default apiService;
