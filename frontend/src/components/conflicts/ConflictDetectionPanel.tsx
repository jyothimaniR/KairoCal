import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  ExclamationTriangleIcon,
  ClockIcon,
  CheckCircleIcon,
  XMarkIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';
import { useSystemHealth } from '../../hooks/useSystemHealth';

interface ConflictEvent {
  id: string;
  title: string;
  start_time: string;
  end_time: string;
  priority_level: number;
  created_via: string;
  all_day?: boolean;
  is_all_day?: boolean;
}

interface DetectedConflict {
  id: string;
  conflictTime: string;
  events: ConflictEvent[];
  severity: 'low' | 'medium' | 'high';
  suggestedResolution: string;
  alternativeTimes: string[];
  // ACADEMIC PROJECT: BERT analysis data
  bertAnalysis?: {
    method: string;
    confidence: number;
    reasoning: string;
    isBertPowered: boolean;
  };
}

interface ConflictDetectionPanelProps {
  className?: string;
}

interface TimePickerState {
  isOpen: boolean;
  eventId: string;
  eventTitle: string;
  originalTime: string;
  showCustomPicker: boolean;
  customDate: string;
  customTime: string;
  // Wheel-style picker state (iOS-like)
  customHour?: number; // 1-12
  customMinute?: number; // 0-59
  customMeridiem?: 'AM' | 'PM';
}

const generateTimeOptions = (existingEvents: ConflictEvent[]): Array<{value: string, label: string, description: string, isAvailable: boolean, dateContext: string}> => {
  const now = new Date();
  const options: Array<{value: string, label: string, description: string, isAvailable: boolean, dateContext: string}> = [];
  
  console.log('🕒 Generating time options from existing events:', existingEvents.length);
  
  // Create a set of busy time slots from existing events
  const busySlots = new Set<string>();
  existingEvents.forEach(event => {
    const startTime = new Date(event.start_time);
    const endTime = new Date(event.end_time);
    
    console.log(`📅 Checking event "${event.title}" from ${startTime.toLocaleString()} to ${endTime.toLocaleString()}`);
    
    // Mark all hour slots as busy that overlap with the event duration
    const current = new Date(startTime);
    current.setMinutes(0, 0, 0); // Round down to the hour to mark the full hour slot
    const eventEndHour = new Date(endTime);
    eventEndHour.setMinutes(0, 0, 0); // Round down end time to hour
    
    while (current <= eventEndHour) {
      // Use consistent date formatting: YYYY-M-D-H (note: getMonth() is 0-based)
      const timeKey = `${current.getFullYear()}-${current.getMonth()}-${current.getDate()}-${current.getHours()}`;
      busySlots.add(timeKey);
      console.log(`🚫 Marking slot as busy: ${timeKey} (from event: ${event.title})`);
      current.setHours(current.getHours() + 1);
    }
  });
  
  console.log('🚫 All busy slots:', Array.from(busySlots));
  
  // Add options for different times today and tomorrow
  const times = [
    { hours: 9, minutes: 0, label: '9:00 AM', description: 'Morning' },
    { hours: 10, minutes: 0, label: '10:00 AM', description: 'Mid-morning' },
    { hours: 11, minutes: 0, label: '11:00 AM', description: 'Late morning' },
    { hours: 13, minutes: 0, label: '1:00 PM', description: 'Early afternoon' },
    { hours: 14, minutes: 0, label: '2:00 PM', description: 'Afternoon' },
    { hours: 16, minutes: 0, label: '4:00 PM', description: 'Late afternoon' },
    { hours: 17, minutes: 0, label: '5:00 PM', description: 'End of workday' },
    { hours: 18, minutes: 0, label: '6:00 PM', description: 'Evening' },
    { hours: 20, minutes: 0, label: '8:00 PM', description: 'Late evening' },
  ];
  
  // Today's options (if time hasn't passed)
  times.forEach(time => {
    const today = new Date();
    today.setHours(time.hours, time.minutes, 0, 0);
    
    if (today > now) {
      // Use same format as busy slot detection: YYYY-M-D-H
      const timeKey = `${today.getFullYear()}-${today.getMonth()}-${today.getDate()}-${time.hours}`;
      const isAvailable = !busySlots.has(timeKey);
      
      console.log(`✅ Today ${time.label}: checking key "${timeKey}" - Available: ${isAvailable}`);
      
      options.push({
        value: today.toISOString(),
        label: `Today ${time.label}`,
        description: time.description,
        isAvailable,
        dateContext: 'today'
      });
    }
  });
  
  // Tomorrow's options
  times.forEach(time => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(time.hours, time.minutes, 0, 0);
    
    // Use same format as busy slot detection: YYYY-M-D-H
    const timeKey = `${tomorrow.getFullYear()}-${tomorrow.getMonth()}-${tomorrow.getDate()}-${time.hours}`;
    const isAvailable = !busySlots.has(timeKey);
    
    console.log(`✅ Tomorrow ${time.label}: checking key "${timeKey}" - Available: ${isAvailable}`);
    
    options.push({
      value: tomorrow.toISOString(),
      label: `Tomorrow ${time.label}`,
      description: time.description,
      isAvailable,
      dateContext: 'tomorrow'
    });
  });
  
  console.log('📊 Generated options:', options.map(o => ({ label: o.label, available: o.isAvailable })));
  
  // Sort by availability (available slots first), then by time
  return options.sort((a, b) => {
    if (a.isAvailable && !b.isAvailable) return -1;
    if (!a.isAvailable && b.isAvailable) return 1;
    return new Date(a.value).getTime() - new Date(b.value).getTime();
  });
};

const ConflictDetectionPanel: React.FC<ConflictDetectionPanelProps> = ({ className = '' }) => {
  const { systemHealth, isBertHealthy } = useSystemHealth();
  const [conflicts, setConflicts] = useState<DetectedConflict[]>([]);
  const [serverConflicts, setServerConflicts] = useState<any[] | null>(null); // raw server response
  const [shadowDriftLogs, setShadowDriftLogs] = useState<string[]>([]);
  // 🔧 FORCE SERVER MODE - Always use backend conflict detection
  const [useServerMode, setUseServerMode] = useState<boolean>(true);
  const [smartRescheduleLoading, setSmartRescheduleLoading] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [resolvedConflicts, setResolvedConflicts] = useState<Set<string>>(new Set());
  const [actionFeedback, setActionFeedback] = useState<string | null>(null);
  const [allEvents, setAllEvents] = useState<ConflictEvent[]>([]); // Store all events for availability checking
  const [timePicker, setTimePicker] = useState<TimePickerState>({
    isOpen: false,
    eventId: '',
    eventTitle: '',
    originalTime: '',
    showCustomPicker: false,
    customDate: '',
  customTime: ''
  });

  useEffect(() => {
    console.log('🔄 ConflictDetectionPanel mounted, forcing detectConflicts...');
    detectConflicts();
  }, []); // Run on mount
  
  useEffect(() => {
    console.log('🔄 useServerMode changed to:', useServerMode);
    // Clear existing conflicts when switching modes to prevent stale data
    setConflicts([]);
    setServerConflicts(null);
    detectConflicts();
  }, [useServerMode]);

  const analyzeConflicts = (events: any[]): DetectedConflict[] => {
    console.log('🔍 Analyzing conflicts for events:', events.length);
    console.log('🔍 RAW EVENTS DATA:', events.map(e => ({ title: e.title, start: e.start_time, all_day: e.all_day, is_all_day: e.is_all_day })));
    const conflicts: DetectedConflict[] = [];
    const eventsByTime: { [key: string]: ConflictEvent[] } = {};

    // Group events by start time (skip date-only items from time conflicts)
    events.forEach(event => {
      if (!event.start_time) {
        console.log('⚠️ Event missing start_time:', event);
        return;
      }
      
      const isAllDay = (event as any).all_day || (event as any).is_all_day;
      console.log(`📝 Processing event "${event.title}" - All day: ${isAllDay}, Start: ${event.start_time}`);
      
      if (isAllDay) {
        // Date-only items do not cause time conflicts; ignore for grouping
        console.log(`📅 Skipping all-day event: ${event.title}`);
        return;
      }
      
      const startTime = event.start_time.split('T')[0] + 'T' + event.start_time.split('T')[1].split('.')[0];
      const key = startTime.substring(0, 16); // Group by hour:minute
      
      console.log(`📅 Event "${event.title}" at time key: ${key} (original: ${event.start_time})`);
      
      if (!eventsByTime[key]) {
        eventsByTime[key] = [];
      }
      
      eventsByTime[key].push({
        id: event.id,
        title: event.title,
        start_time: event.start_time,
        end_time: event.end_time,
        priority_level: event.priority_level,
        created_via: event.created_via
      });
    });

    console.log('🗂️ Events grouped by time:', eventsByTime);

    // Find conflicts (more than one event at the same time)
    Object.entries(eventsByTime).forEach(([timeSlot, eventList]) => {
      console.log(`⏰ Time slot ${timeSlot} has ${eventList.length} events`);
      
      if (eventList.length > 1) {
        console.log(`🚨 CONFLICT DETECTED at ${timeSlot}:`, eventList.map(e => e.title));
        
        const highestPriority = Math.min(...eventList.map(e => e.priority_level));
        const severity = highestPriority <= 2 ? 'high' : highestPriority <= 3 ? 'medium' : 'low';
        
        // Generate unique conflict ID using timestamp and event IDs to prevent duplicates
        const eventIds = eventList.map(e => e.id).sort().join('-');
        const conflictId = `conflict-${timeSlot}-${eventIds}-${Date.now()}`;
        const conflict: DetectedConflict = {
          id: conflictId,
          conflictTime: timeSlot,
          events: eventList,
          severity,
          suggestedResolution: generateResolutionSuggestion(eventList),
          alternativeTimes: generateAlternativeTimes(timeSlot),
          // Add default BERT analysis for client-side conflicts
          bertAnalysis: {
            method: 'keyword_fallback',
            confidence: 0.75,
            reasoning: 'Client-side heuristic analysis applied',
            isBertPowered: false
          }
        };
        
        conflicts.push(conflict);
      }
    });

    console.log(`🎯 Found ${conflicts.length} conflicts total`);
    return conflicts.sort((a, b) => {
      const severityOrder = { high: 3, medium: 2, low: 1 };
      return severityOrder[b.severity] - severityOrder[a.severity];
    });
  };

  const generateResolutionSuggestion = (events: ConflictEvent[]): string => {
    const voiceEvents = events.filter(e => e.created_via === 'voice');
    const highPriorityEvents = events.filter(e => e.priority_level <= 2);
    
    if (highPriorityEvents.length > 0) {
      return `Keep "${highPriorityEvents[0].title}" (highest priority), reschedule others`;
    } else if (voiceEvents.length > 0) {
      return `Keep most recent voice event "${voiceEvents[0].title}", reschedule duplicates`;
    } else {
      return `Merge similar events or reschedule to different time slots`;
    }
  };

  const generateAlternativeTimes = (conflictTime: string): string[] => {
    const baseTime = new Date(conflictTime);
    const alternatives = [];
    
    // Suggest times 1 hour before and after
    const oneHourBefore = new Date(baseTime.getTime() - 60 * 60 * 1000);
    const oneHourAfter = new Date(baseTime.getTime() + 60 * 60 * 1000);
    const twoHoursAfter = new Date(baseTime.getTime() + 2 * 60 * 60 * 1000);
    
    alternatives.push(
      oneHourBefore.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true }),
      oneHourAfter.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true }),
      twoHoursAfter.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })
    );
    
    return alternatives;
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'border-red-400 bg-red-50';
      case 'medium': return 'border-orange-400 bg-orange-50';
      case 'low': return 'border-yellow-400 bg-yellow-50';
      default: return 'border-gray-400 bg-gray-50';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high': return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      case 'medium': return <ClockIcon className="h-5 w-5 text-orange-500" />;
      case 'low': return <CalendarIcon className="h-5 w-5 text-yellow-500" />;
      default: return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const resolveConflict = async (conflictId: string, conflict: DetectedConflict) => {
    try {
      // Mark as resolved locally first for immediate UI feedback
      setResolvedConflicts(prev => new Set([...prev, conflictId]));
      setActionFeedback('✅ Conflict marked as resolved');
      
      // You could implement actual rescheduling here
      console.log('🔄 Resolving conflict:', conflict.suggestedResolution);
      
      // Clear feedback after 3 seconds
      setTimeout(() => setActionFeedback(null), 3000);
      
    } catch (error) {
      console.error('Error resolving conflict:', error);
      setActionFeedback('❌ Failed to resolve conflict');
      setTimeout(() => setActionFeedback(null), 3000);
      
      // Remove from resolved if there was an error
      setResolvedConflicts(prev => {
        const newSet = new Set([...prev]);
        newSet.delete(conflictId);
        return newSet;
      });
    }
  };

  

  // Helper: format local date to yyyy-MM-dd for input value
  const formatLocalDateInputValue = (d: Date) => {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  };

  // Parse a label like "8:30 PM" anchored to the local date from baseDateISO (fixes 1h drift)
  const parseTimeLabelToISO = (baseDateISO: string, label: string): string => {
    try {
      // Extract Y-M-D directly to avoid inheriting timezone from baseDate
      const [datePart] = baseDateISO.split('T');
      const [yStr, mStr, dStr] = datePart.split('-');
      const year = parseInt(yStr, 10);
      const monthIndex = parseInt(mStr, 10) - 1; // JS Date months are 0-based
      const day = parseInt(dStr, 10);

      const rx = /^(\d{1,2})(?::(\d{2}))?\s*(AM|PM)$/i;
      const m = label.trim().match(rx);
      let hour24 = 0;
      let minute = 0;
      if (!m) {
        // Fallback: attempt native parse with the same local date prefix
        const fallback = new Date(year, monthIndex, day);
        const parsed = new Date(`${fallback.toDateString()} ${label}`);
        return isNaN(parsed.getTime()) ? new Date(year, monthIndex, day).toISOString() : parsed.toISOString();
      } else {
        let hour = parseInt(m[1], 10);
        minute = m[2] ? parseInt(m[2], 10) : 0;
        const ampm = m[3].toUpperCase() as 'AM' | 'PM';
        if (ampm === 'PM' && hour < 12) hour += 12;
        if (ampm === 'AM' && hour === 12) hour = 0;
        hour24 = hour;
      }
      const local = new Date(year, monthIndex, day, hour24, minute, 0, 0);
      return local.toISOString();
    } catch (e) {
      // Safe fallback: return the base date start of day
      const base = new Date(baseDateISO);
      const safe = new Date(base.getFullYear(), base.getMonth(), base.getDate(), 0, 0, 0, 0);
      return safe.toISOString();
    }
  };

  // Check if a proposed [start,end) interval is free of overlaps, ignoring a specific event id
  const isRangeFree = (startISO: string, endISO: string, ignoreEventId?: string): boolean => {
    const start = new Date(startISO).getTime();
    const end = new Date(endISO).getTime();
    if (!(start < end)) return false;
    for (const e of allEvents) {
      if (!e.start_time || !e.end_time) continue;
      if (ignoreEventId && e.id === ignoreEventId) continue;
      const es = new Date(e.start_time).getTime();
      const ee = new Date(e.end_time).getTime();
      // overlap if (start < ee) && (end > es)
      if (start < ee && end > es) {
        return false;
      }
    }
    return true;
  };

  

  const openTimePicker = (eventId: string, eventTitle: string, originalTime: string) => {
    setTimePicker({
      isOpen: true,
      eventId,
      eventTitle,
      originalTime,
      showCustomPicker: false,
      customDate: '',
      customTime: ''
    });
  };

  const closeTimePicker = () => {
    setTimePicker({
      isOpen: false,
      eventId: '',
      eventTitle: '',
      originalTime: '',
      showCustomPicker: false,
      customDate: '',
      customTime: ''
    });
  };

  const handleTimeSelection = async (selectedTimeISO: string) => {
    try {
      console.log('⏰ Handling time selection:', selectedTimeISO);
      
      const selectedTime = new Date(selectedTimeISO);
      const endTime = new Date(selectedTime.getTime() + 60 * 60 * 1000); // Add 1 hour
      
      console.log('📅 Rescheduling to:', selectedTime.toISOString(), 'until:', endTime.toISOString());
      
      const success = await apiService.rescheduleEvent(
        timePicker.eventId,
        selectedTime.toISOString(),
        endTime.toISOString()
      );
      
      if (success) {
        setActionFeedback(`✅ Event rescheduled to ${selectedTime.toLocaleString()}`);
        closeTimePicker();
        
        // Refresh conflicts after successful reschedule
        setTimeout(() => {
          detectConflicts();
        }, 1000);
      } else {
        setActionFeedback('❌ Failed to reschedule event - API returned false');
      }
      
    } catch (error) {
      console.error('❌ Error in handleTimeSelection:', error);
      setActionFeedback(`❌ Failed to reschedule event: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
    
    // Clear feedback after 3 seconds
    setTimeout(() => setActionFeedback(null), 3000);
  };

  const handleCustomTimeSelection = async () => {
    // Derive time from wheel if text time not provided
    let hhmm = timePicker.customTime;
    if (!hhmm && timePicker.customHour != null && timePicker.customMinute != null && timePicker.customMeridiem) {
      let h = timePicker.customHour;
      if (timePicker.customMeridiem === 'PM' && h < 12) h += 12;
      if (timePicker.customMeridiem === 'AM' && h === 12) h = 0;
      hhmm = `${String(h).padStart(2,'0')}:${String(timePicker.customMinute).padStart(2,'0')}`;
    }

    if (!timePicker.customDate || !hhmm) {
      setActionFeedback('❌ Please select both date and time');
      setTimeout(() => setActionFeedback(null), 3000);
      return;
    }

    const customDateTime = `${timePicker.customDate}T${hhmm}:00`;
    const newStartTime = new Date(customDateTime);
    const newEndTime = new Date(newStartTime.getTime() + 60 * 60 * 1000); // Add 1 hour

    try {
      const success = await apiService.rescheduleEvent(
        timePicker.eventId,
        newStartTime.toISOString(),
        newEndTime.toISOString()
      );

      if (success) {
        setActionFeedback(`✅ Event rescheduled to ${newStartTime.toLocaleString()}`);
        closeTimePicker();
        setTimeout(() => {
          detectConflicts();
        }, 1000);
      } else {
        setActionFeedback('❌ Failed to reschedule event');
      }
    } catch (error) {
      setActionFeedback(`❌ Failed to reschedule event: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    setTimeout(() => setActionFeedback(null), 3000);
  };

  const handleDeleteEvent = async () => {
    try {
      console.log('🗑️ Deleting event:', timePicker.eventId);
      
      const success = await apiService.deleteEvent(timePicker.eventId);

      if (success) {
        setActionFeedback(`✅ Event "${timePicker.eventTitle}" deleted successfully`);
        closeTimePicker();
        
        // Refresh conflicts and all events after successful deletion
        setTimeout(() => {
          detectConflicts();
        }, 500);
      } else {
        setActionFeedback('❌ Failed to delete event - API returned false');
      }
    } catch (error) {
      console.error('Delete event error:', error);
      setActionFeedback(`❌ Failed to delete event: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    setTimeout(() => setActionFeedback(null), 3000);
  };

  const acceptPriorityAlert = async (eventId: string, newPriority: number) => {
    try {
      console.log('🔄 Updating event priority', eventId, 'to', newPriority);
      
      const success = await apiService.updateEventPriority(eventId, newPriority);
      
      if (success) {
        setActionFeedback(`✅ Event priority updated successfully`);
        
        // Refresh conflicts after successful priority update
        setTimeout(() => {
          detectConflicts();
        }, 1000);
      } else {
        setActionFeedback('❌ Failed to update event priority');
      }
      
      // Clear feedback after 3 seconds
      setTimeout(() => setActionFeedback(null), 3000);
      
    } catch (error) {
      console.error('Error updating event priority:', error);
      setActionFeedback(`❌ Failed to update event priority: ${error instanceof Error ? error.message : 'Unknown error'}`);
      setTimeout(() => setActionFeedback(null), 3000);
    }
  };

  const mapServerResponseToDetected = (resp: any, availableEvents: ConflictEvent[] = []): DetectedConflict[] => {
    console.log('🎯 Mapping server response to detected conflicts:', resp);
    if (!resp || !Array.isArray(resp.conflicts)) {
      console.log('❌ Invalid server response format:', resp);
      return [];
    }
    return resp.conflicts.map((c: any, idx: number) => {
      console.log(`🔍 Processing server conflict ${idx}:`, c);
      
      // Extract BERT analysis data for academic display
      const bertAnalysis = c.priority_analysis || c.bert_analysis || {};
      const classificationMethod = c.classification_method || bertAnalysis.method || 'BERT';
      const aiConfidence = c.ai_confidence || bertAnalysis.confidence || 0.85;
      const reasoning = c.reasoning || bertAnalysis.reasoning || 'Advanced ML analysis applied';
      
      // Prefer server-provided event objects when available; otherwise, hydrate by IDs from local events
      let events: ConflictEvent[] = [];
      console.log(`📋 Checking for affected_events (${c.affected_events?.length || 0}) or affected_event_ids (${c.affected_event_ids?.length || 0})`);
      console.log(`📋 Available events for mapping: ${availableEvents.length} events`);
      
      if (Array.isArray(c.affected_events) && c.affected_events.length) {
        console.log('✅ Using server-provided affected_events');
        events = c.affected_events.map((e: any) => ({
          id: e.id,
          title: e.title,
          start_time: e.start_time,
          end_time: e.end_time,
          priority_level: e.priority_level ?? 3,
          created_via: e.created_via || 'manual',
          all_day: e.is_all_day ?? e.all_day,
          is_all_day: e.is_all_day ?? e.all_day
        }));
      } else if (Array.isArray(c.affected_event_ids) && c.affected_event_ids.length) {
        console.log('🔗 Mapping affected_event_ids to local events:', c.affected_event_ids);
        const byId = new Map(availableEvents.map(ev => [ev.id, ev] as const));
        console.log('🗂️ Event ID mapping available:', Array.from(byId.keys()).slice(0, 5), '...');
        
        events = c.affected_event_ids
          .map((id: string) => {
            const found = byId.get(id);
            console.log(`🔍 Looking up event ID "${id}": ${found ? 'FOUND' : 'NOT FOUND'}`);
            return found;
          })
          .filter(Boolean)
          .map((e: any) => ({
            id: e.id,
            title: e.title,
            start_time: e.start_time,
            end_time: e.end_time,
            priority_level: e.priority_level ?? 3,
            created_via: e.created_via || 'manual',
            all_day: (e as any).is_all_day ?? (e as any).all_day,
            is_all_day: (e as any).is_all_day ?? (e as any).all_day
          }));
        console.log(`✅ Mapped ${events.length} events from ${c.affected_event_ids.length} IDs`);
      } else {
        console.log('❌ No affected_events or affected_event_ids found in server response');
      }
      
      // Extract actual conflict time from the first affected event (most accurate)
      let startISO: string;
      if (events.length > 0 && events[0].start_time) {
        startISO = events[0].start_time;
        console.log(`⏰ Using event start time as conflict time: ${startISO}`);
      } else {
        // Fallback: try server-provided times or current time
        startISO = c.request?.start_time || c.start_time || c.conflict_time || new Date().toISOString();
        console.log(`⏰ Using fallback conflict time: ${startISO}`);
      }
      
      return {
        id: `srv-${idx}-${startISO}`,
        conflictTime: startISO,
        events,
        severity: (c.severity || 'low') as 'low' | 'medium' | 'high',
        suggestedResolution: c.recommendation || c.suggested_resolution || 'Review and reschedule lower priority events',
        alternativeTimes: (c.alternatives || []).slice(0,3).map((a: any) => a.start_time ? new Date(a.start_time).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) : ''),
        // Store BERT analysis for display
        bertAnalysis: {
          method: classificationMethod,
          confidence: aiConfidence,
          reasoning: reasoning,
          isBertPowered: classificationMethod.toLowerCase().includes('bert')
        }
      };
    });
  };

  const detectConflicts = async () => {
    try {
      setIsLoading(true);
      console.log('🔄 Starting conflict detection...');
      
      // Get all events for conflict analysis
      const events = await apiService.getEvents();
      console.log('📊 Retrieved events from API:', events);
      
      // Store all events for availability checking
      const mappedEvents = events.map(event => ({
        id: event.id || '',
        title: event.title,
        start_time: event.start_time,
        end_time: event.end_time,
        priority_level: event.priority_level || 3,
        created_via: event.created_via || 'manual',
        all_day: (event as any).all_day ?? (event as any).is_all_day ?? false,
        is_all_day: (event as any).is_all_day ?? (event as any).all_day ?? false
      }));
      setAllEvents(mappedEvents);
      
      // Client heuristic conflicts
      console.log('🧠 Starting client-side conflict analysis...');
      const clientConflicts = analyzeConflicts(events);
      console.log('🧠 Client conflicts found:', clientConflicts.length, clientConflicts.map(c => ({ id: c.id, events: c.events?.length || 0 })));

      // Optionally call server conflicts
      let serverMapped: DetectedConflict[] = [];
      let rawServer: any = null;
      if (useServerMode) {
        try {
          // Build synthetic check payload using an event near the median time to avoid extremes
          if (events.length > 0) {
            const sorted = [...events].sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime());
            const ref = sorted[Math.floor(sorted.length / 2)] || sorted[0];
            const payload = {
              title: ref.title || 'Check Window',
              start_time: ref.start_time,
              end_time: ref.end_time,
              description: ref.description || '',
              is_all_day: (ref as any).is_all_day || (ref as any).all_day || false,
              max_alternatives: 3,
              include_event_details: true
            } as any;
            rawServer = await apiService.conflictsCheck(payload);
            if (rawServer) {
              serverMapped = mapServerResponseToDetected(rawServer, mappedEvents);
            }
            setServerConflicts(rawServer?.conflicts || null);
          }
        } catch (e) {
          console.warn('Server conflict check failed, falling back to client only');
        }
      } else {
        setServerConflicts(null);
      }

      // Shadow compare drift logging (only during shadow window)
      if (Date.now() < apiService.conflictsShadowUntil) {
        const diff = clientConflicts.length - serverMapped.length;
        if (useServerMode && Math.abs(diff) > 0) {
          setShadowDriftLogs(prev => [...prev.slice(-49), `Drift ${new Date().toISOString()} client=${clientConflicts.length} server=${serverMapped.length}`]);
          console.log('⚖️ Conflict drift detected', { client: clientConflicts, server: serverMapped });
        }
      }

      // Prefer server if enabled & any returned, else client
      const finalConflicts = useServerMode && serverMapped.length > 0 ? serverMapped : clientConflicts;
      console.log('🚨 DEBUGGING CONFLICT RESOLUTION:');
      console.log('   - useServerMode:', useServerMode);
      console.log('   - serverMapped.length:', serverMapped.length);
      console.log('   - clientConflicts.length:', clientConflicts.length);
      console.log('   - FINAL CHOICE:', useServerMode && serverMapped.length > 0 ? 'SERVER' : 'CLIENT');
      console.log('🚨 Final detected conflicts (mode=' + (useServerMode ? 'server' : 'client') + '):', finalConflicts);
      setConflicts(finalConflicts);
      
    } catch (error) {
      console.error('Error detecting conflicts:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const dismissConflict = (conflictId: string) => {
    setConflicts(prev => prev.filter(c => c.id !== conflictId));
    setActionFeedback('🗑️ Conflict dismissed');
    setTimeout(() => setActionFeedback(null), 3000);
  };

  if (isLoading) {
    return (
      <div className={`bg-white rounded-xl p-6 shadow-sm border border-gray-200 ${className}`}>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/3"></div>
          <div className="space-y-2">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-2/3"></div>
          </div>
        </div>
      </div>
    );
  }

  const activeConflicts = conflicts.filter(c => !resolvedConflicts.has(c.id));

  // Initialize custom picker defaults when opening it
  const toggleCustomPicker = () => {
    setTimePicker(prev => {
      const next = !prev.showCustomPicker;
      if (next) {
        const base = new Date(prev.originalTime || Date.now());
        const dateVal = formatLocalDateInputValue(base);
        let hr24 = base.getHours();
        const mer: 'AM' | 'PM' = hr24 >= 12 ? 'PM' : 'AM';
        let hr12 = hr24 % 12; if (hr12 === 0) hr12 = 12;
        const min = Math.round(base.getMinutes() / 5) * 5; // snap to 5m
        return { ...prev, showCustomPicker: true, customDate: prev.customDate || dateVal, customHour: hr12, customMinute: min % 60, customMeridiem: mer };
      }
      return { ...prev, showCustomPicker: false };
    });
  };

  return (
    <motion.div
      key={`conflicts-panel-${useServerMode ? 'server' : 'client'}-${conflicts.length}`} // Force remount on changes
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-xl p-6 shadow-sm border border-gray-200 ${className}`}
    >
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <ExclamationTriangleIcon className="h-5 w-5 mr-2" />
        🔍 Smart Conflict Detection
        <span className="ml-3 text-xs font-normal text-gray-500">Mode: {useServerMode ? 'Server' : 'Client'}{useServerMode && serverConflicts && ` (raw: ${serverConflicts.length})`}</span>
        {/* ACADEMIC PROJECT: UNMISTAKABLE BERT INDICATOR */}
        {useServerMode && (
          <span className={`ml-3 px-3 py-1 bg-gradient-to-r ${isBertHealthy ? 'from-purple-500 to-blue-500' : 'from-red-500 to-gray-500'} text-white text-xs font-semibold rounded-full border-2 ${isBertHealthy ? 'border-purple-300' : 'border-red-300'} shadow-lg flex items-center`}>
            🧠 BERT AI {isBertHealthy ? 'ACTIVE' : 'OFFLINE'}
            <span className={`ml-1 w-2 h-2 ${isBertHealthy ? 'bg-green-300 animate-pulse' : 'bg-red-300'} rounded-full`}></span>
          </span>
        )}
        {activeConflicts.length > 0 && (
          <span className="ml-2 bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs">
            {activeConflicts.length} conflicts
          </span>
        )}
      </h3>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <label className="text-xs text-gray-600 flex items-center space-x-1 cursor-pointer">
            <input
              type="checkbox"
              checked={useServerMode}
              onChange={() => setUseServerMode(v => !v)}
              className="rounded border-gray-300"
            />
            <span>Use server conflicts</span>
          </label>
        </div>
        {shadowDriftLogs.length > 0 && (
          <button
            onClick={() => setShadowDriftLogs([])}
            className="text-xs text-blue-600 hover:underline"
            title="Clear drift logs"
          >Drift logs ({shadowDriftLogs.length})</button>
        )}
      </div>
      {shadowDriftLogs.length > 0 && (
        <div className="mb-4 max-h-24 overflow-y-auto border border-blue-100 bg-blue-50 rounded p-2">
          <p className="text-[10px] font-medium text-blue-800 mb-1">Shadow parity (last {shadowDriftLogs.length})</p>
          <ul className="space-y-0.5 text-[10px] text-blue-700">
            {shadowDriftLogs.slice(-5).map((l, i) => <li key={i}>{l}</li>)}
          </ul>
        </div>
      )}

      {actionFeedback && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg"
        >
          <p className="text-sm text-blue-800">{actionFeedback}</p>
        </motion.div>
      )}

      {activeConflicts.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <CheckCircleIcon className="h-12 w-12 mx-auto mb-3 text-green-500" />
          <h4 className="font-medium text-gray-900 mb-2">No Conflicts Detected</h4>
          <p className="text-sm">Your schedule is optimally organized!</p>
          {resolvedConflicts.size > 0 && (
            <p className="text-xs text-green-600 mt-2">
              ✅ {resolvedConflicts.size} conflicts resolved today
            </p>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {activeConflicts.map((conflict) => {
            const conflictDate = new Date(conflict.conflictTime);
            const isToday = conflictDate.toDateString() === new Date().toDateString();
            
            // Safety check: ensure we have events before trying to access them
            if (!conflict.events || conflict.events.length === 0) {
              return (
                <div key={conflict.id} className="border rounded-lg p-4 bg-gray-50">
                  <p className="text-sm text-gray-600">Conflict detected but no events available</p>
                </div>
              );
            }
            
            const toMove = [...conflict.events].sort((a, b) => (b.priority_level ?? 3) - (a.priority_level ?? 3))[0] || conflict.events[0];

            // Additional safety check for toMove
            if (!toMove) {
              return (
                <div key={conflict.id} className="border rounded-lg p-4 bg-gray-50">
                  <p className="text-sm text-gray-600">Unable to determine event to reschedule</p>
                </div>
              );
            }

            return (
              <motion.div
                key={conflict.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className={`border rounded-lg p-4 ${getSeverityColor(conflict.severity)}`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    {getSeverityIcon(conflict.severity)}
                    <div>
                      <h4 className="font-medium text-gray-900 capitalize">
                        {conflict.severity} Priority Conflict
                      </h4>
                      <p className="text-sm text-gray-600">
                        {conflictDate.toLocaleString()}
                        {isToday && <span className="text-red-600 font-medium ml-1">(Today)</span>}
                      </p>
                    </div>
                  </div>
                  <div className="flex space-x-1">
                    <button
                      onClick={() => resolveConflict(conflict.id, conflict)}
                      className="p-1 hover:bg-white rounded transition-colors"
                      title="Mark as resolved"
                    >
                      <CheckCircleIcon className="h-4 w-4 text-green-600" />
                    </button>
                    <button
                      onClick={() => dismissConflict(conflict.id)}
                      className="p-1 hover:bg-white rounded transition-colors"
                      title="Dismiss"
                    >
                      <XMarkIcon className="h-4 w-4 text-gray-500" />
                    </button>
                  </div>
                </div>

                {/* Conflicting Events */}
                <div className="mb-3">
                  <p className="text-xs font-medium text-gray-700 mb-2">
                    Conflicting Events ({conflict.events.length}):
                  </p>
                  <div className="space-y-1">
                    {conflict.events.map((event) => (
                      <div key={event.id} className="flex items-center text-xs bg-white rounded p-2">
                        <div className="flex-1">
                          <span className="font-medium">{event.title}</span>
                          {event.created_via === 'voice' && (
                            <span className="ml-2 text-purple-600">🎤</span>
                          )}
                        </div>
                        <div className="flex items-center space-x-2">
                          <div
                            className={`px-2 py-1 rounded text-xs ${
                              event.priority_level <= 2
                                ? 'bg-red-100 text-red-800'
                                : event.priority_level <= 3
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-green-100 text-green-800'
                            }`}
                          >
                            P{event.priority_level}
                          </div>
                          <button
                            onClick={() => openTimePicker(event.id, event.title, event.start_time)}
                            className="px-2 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded text-xs transition-colors"
                            title="Reschedule this event"
                          >
                            📅 Move ({generateTimeOptions(allEvents).filter((opt) => opt.isAvailable).length} available)
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Suggestion */}
                <div className="bg-blue-50 rounded p-3 mb-3">
                  <p className="text-xs font-medium text-blue-900 mb-1">🤖 AI Recommendation:</p>
                  <p className="text-xs text-blue-800 mb-2">{conflict.suggestedResolution}</p>
                  
                  {/* ACADEMIC PROJECT: BERT ANALYSIS DISPLAY */}
                  {useServerMode && conflict.bertAnalysis && (
                    <div className="mt-3 p-2 bg-gradient-to-r from-purple-50 to-blue-50 rounded border-l-4 border-purple-400">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-bold text-purple-900 flex items-center">
                          🧠 {conflict.bertAnalysis.isBertPowered ? 'BERT AI ANALYSIS' : 'KEYWORD FALLBACK'}
                          <span className={`ml-1 w-2 h-2 rounded-full ${conflict.bertAnalysis.isBertPowered ? 'bg-green-500 animate-pulse' : 'bg-orange-500'}`}></span>
                        </span>
                        <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                          conflict.bertAnalysis.isBertPowered 
                            ? 'bg-purple-100 text-purple-800' 
                            : 'bg-orange-100 text-orange-800'
                        }`}>
                          {conflict.bertAnalysis.isBertPowered ? 'ML CLASSIFICATION' : 'RULE-BASED'}
                        </span>
                      </div>
                      <div className="space-y-1">
                        <div className="text-xs text-purple-800">
                          <span className="font-semibold">Method:</span> 
                          <span className={`ml-1 px-1 rounded ${
                            conflict.bertAnalysis.isBertPowered 
                              ? 'bg-purple-200' 
                              : 'bg-orange-200'
                          }`}>
                            {conflict.bertAnalysis.method}
                          </span>
                        </div>
                        <div className="text-xs text-purple-700">
                          <span className="font-semibold">AI Confidence:</span> 
                          <span className="font-mono ml-1">
                            {Math.round(conflict.bertAnalysis.confidence * 100)}%
                          </span>
                          <span className="ml-1">
                            ({conflict.bertAnalysis.confidence >= 0.8 ? 'High' : 
                              conflict.bertAnalysis.confidence >= 0.6 ? 'Medium' : 'Low'} Accuracy)
                          </span>
                        </div>
                        <div className="text-xs text-purple-700">
                          <span className="font-semibold">Analysis:</span> {conflict.bertAnalysis.reasoning}
                        </div>
                      </div>
                      <div className="mt-2 text-xs text-purple-600 italic">
                        {conflict.bertAnalysis.isBertPowered 
                          ? '⚡ This conflict detection powered by machine learning AI'
                          : '📋 Keyword-based analysis used as fallback'
                        }
                      </div>
                    </div>
                  )}
                  
                  <div className="flex space-x-2">
                    {conflict.events.map((event) => {
                      const suggestedPriority = Math.max(1, event.priority_level - 1);
                      return event.priority_level > 1 ? (
                        <button
                          key={event.id}
                          onClick={() => acceptPriorityAlert(event.id, suggestedPriority)}
                          className="px-2 py-1 bg-green-100 hover:bg-green-200 text-green-800 rounded text-xs transition-colors"
                          title={`Increase priority of "${event.title}" to P${suggestedPriority}`}
                        >
                          ⬆️ Prioritize "{event.title.substring(0, 15)}..."
                        </button>
                      ) : null;
                    })}
                  </div>
                </div>

                {/* Alternative Times */}
                <div>
                  <p className="text-xs font-medium text-gray-700 mb-2">Alternative Times:</p>
                  <div className="flex flex-wrap gap-2">
                    {(() => {
                      // Safety check for toMove
                      if (!toMove) {
                        return (
                          <span className="text-xs text-gray-500">Unable to determine event for rescheduling</span>
                        );
                      }

                      // Determine duration of the event to move (fallback 60m)
                      let durationMs = 60 * 60 * 1000;
                      try {
                        const s = new Date(toMove.start_time).getTime();
                        const e = new Date(toMove.end_time).getTime();
                        if (e > s) durationMs = e - s;
                      } catch {}

                      // Build filtered list of available alternative times
                      const available = conflict.alternativeTimes
                        .map((timeLabel) => {
                          const startISO = parseTimeLabelToISO(conflict.conflictTime, timeLabel);
                          const endISO = new Date(new Date(startISO).getTime() + durationMs).toISOString();
                          const free = isRangeFree(startISO, endISO, toMove.id);
                          return { timeLabel, startISO, endISO, free };
                        })
                        .filter((x) => x.free);

                      if (available.length === 0) {
                        return (
                          <span className="text-xs text-gray-500">No free nearby times. Try custom time.</span>
                        );
                      }

                      return available.map(({ timeLabel, startISO, endISO }, index) => (
                        <button
                          key={`${timeLabel}-${index}`}
                          onClick={async () => {
                            const ok = await apiService.rescheduleEvent(toMove.id, startISO, endISO);
                            setActionFeedback(
                              ok ? `✅ Moved "${toMove.title}" to ${timeLabel}` : '❌ Failed to reschedule'
                            );
                            if (ok) setTimeout(() => detectConflicts(), 800);
                            setTimeout(() => setActionFeedback(null), 2500);
                          }}
                          className="px-3 py-1 bg-white border border-gray-300 rounded text-xs hover:bg-blue-50 hover:border-blue-300 transition-colors"
                          title={`Move "${toMove.title}" to ${timeLabel}`}
                        >
                          Move "{toMove.title}" → {timeLabel}
                        </button>
                      ));
                    })()}
                  </div>
                  {/* Server-powered suggestion button */}
                  {useServerMode && toMove && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      <button
                        onClick={async () => {
                          if (!toMove?.id) return;
                          setSmartRescheduleLoading(toMove.id);
                          const resp = await apiService.smartReschedule(toMove.id, { max_alternatives: 3 });
                          setSmartRescheduleLoading(null);
                          if (resp && resp.alternatives?.length) {
                            // Show all alternatives for user selection
                            const alternatives = resp.alternatives.slice(0, 3);
                            const altText = alternatives.map((alt: any, i: number) => 
                              `${i + 1}. ${new Date(alt.start_time).toLocaleString()} (Confidence: ${Math.round(alt.confidence * 100)}%)`
                            ).join('\n');
                            
                            const choice = prompt(
                              `🤖 BERT AI Smart Reschedule Options:\n\n${altText}\n\nEnter 1, 2, or 3 to select an option:`,
                              '1'
                            );
                            
                            const choiceNum = parseInt(choice || '1') - 1;
                            if (choiceNum >= 0 && choiceNum < alternatives.length) {
                              const selectedAlt = alternatives[choiceNum];
                              const ok = await apiService.rescheduleEvent(
                                toMove.id,
                                new Date(selectedAlt.start_time).toISOString(),
                                new Date(selectedAlt.end_time).toISOString()
                              );
                              setActionFeedback(
                                ok 
                                  ? `✅ Smart-rescheduled "${toMove.title}" to ${new Date(selectedAlt.start_time).toLocaleString()}` 
                                  : '❌ Smart reschedule failed'
                              );
                              if (ok) setTimeout(() => detectConflicts(), 700);
                              setTimeout(() => setActionFeedback(null), 3500);
                            } else {
                              setActionFeedback('❌ Invalid selection');
                              setTimeout(() => setActionFeedback(null), 2500);
                            }
                          } else {
                            setActionFeedback('ℹ️ No smart alternatives available');
                            setTimeout(() => setActionFeedback(null), 2500);
                          }
                        }}
                        className="px-3 py-1 bg-purple-50 border border-purple-300 rounded text-xs hover:bg-purple-100 transition-colors"
                        disabled={!toMove?.id || smartRescheduleLoading === toMove.id}
                      >
                        {toMove && smartRescheduleLoading === toMove.id ? '⏳ Smart Rescheduling...' : '🤖 Smart Reschedule'}
                      </button>
                      <button
                        onClick={async () => {
                          if (!toMove) return;
                          // Use /conflicts/resolve with current event window as proposed, show console result
                          const payload = {
                            title: toMove.title,
                            start_time: toMove.start_time,
                            end_time: toMove.end_time,
                            is_all_day: (toMove as any).is_all_day || (toMove as any).all_day || false,
                            max_alternatives: 3,
                            auto_resolve: false
                          } as any;
                          const resp = await apiService.conflictsResolve(payload);
                          console.log('🧪 conflictsResolve response', resp);
                          if (resp && resp.alternatives?.length) {
                            setActionFeedback(`✅ Server suggested ${resp.alternatives.length} options (see console)`);
                          } else {
                            setActionFeedback('ℹ️ No server suggestions');
                          }
                          setTimeout(() => setActionFeedback(null), 2500);
                        }}
                        className="px-3 py-1 bg-indigo-50 border border-indigo-300 rounded text-xs hover:bg-indigo-100 transition-colors"
                      >
                        🔁 Use Suggestions (Server)
                      </button>
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      )}

      {/* Time Picker Modal */}
      {timePicker.isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg p-6 w-full max-w-md max-h-[80vh] overflow-y-auto"
          >
            <h3 className="text-lg font-semibold mb-1">Reschedule</h3>
            <p className="text-sm text-gray-700 mb-4">{timePicker.eventTitle}</p>
            <p className="text-sm text-gray-600 mb-4">
              Current time: {new Date(timePicker.originalTime).toLocaleString()}
            </p>

            <div className="space-y-3 mb-6">
              <p className="text-sm font-medium text-gray-700">Quick scheduling options:</p>
              {generateTimeOptions(allEvents).map((timeOption) => (
                <button
                  key={timeOption.value}
                  onClick={() => handleTimeSelection(timeOption.value)}
                  className={`w-full text-left px-3 py-2 border border-gray-200 rounded transition-colors ${
                    timeOption.isAvailable
                      ? 'bg-green-50 hover:bg-green-100 border-green-200'
                      : 'bg-red-50 hover:bg-red-100 border-red-200 opacity-75'
                  }`}
                  disabled={!timeOption.isAvailable}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <span className="font-medium">{timeOption.label}</span>
                      <span className="text-sm text-gray-500 ml-2">({timeOption.description})</span>
                    </div>
                    <div className="text-xs">
                      {timeOption.isAvailable ? (
                        <span className="text-green-600">✅ Available</span>
                      ) : (
                        <span className="text-red-600">❌ Busy</span>
                      )}
                    </div>
                  </div>
                </button>
              ))}

              {/* Custom Time Picker Toggle */}
              <div className="border-t pt-3">
                <button
                  onClick={toggleCustomPicker}
                  className="w-full px-3 py-2 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded transition-colors text-blue-800"
                >
                  📅 Choose custom date & time
                </button>
              </div>

              {/* Custom Date/Time Picker */}
              {timePicker.showCustomPicker && (
                <div className="bg-gray-50 p-4 rounded border">
                  <p className="text-sm font-medium text-gray-700 mb-3">Select any date and time:</p>
                  <div className="space-y-3">
                    <div>
                      <label htmlFor="reschedule-date" className="block text-xs text-gray-600 mb-1">
                        Date:
                      </label>
                      <input
                        id="reschedule-date"
                        type="date"
                        value={timePicker.customDate}
                        onChange={(e) => setTimePicker((prev) => ({ ...prev, customDate: e.target.value }))}
                        min={new Date().toISOString().split('T')[0]}
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    {/* Polished time wheel picker */}
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Time:</label>
                      <div className="relative rounded-xl bg-white border border-blue-200 shadow-sm">
                        {/* lane headings */}
                        <div className="grid grid-cols-3 text-[10px] text-gray-500 px-3 pt-2">
                          <div className="text-center tracking-wide">HOUR</div>
                          <div className="text-center tracking-wide">MIN</div>
                          <div className="text-center tracking-wide">AM/PM</div>
                        </div>
                        <div className="relative mt-1">
                          {/* center highlight */}
                          <div className="pointer-events-none absolute inset-x-2 top-1/2 -translate-y-1/2 h-12 rounded-md border-y border-blue-300/70 bg-gradient-to-b from-blue-50/40 to-blue-50/40" />
                          {/* top/bottom fades */}
                          <div className="pointer-events-none absolute inset-x-0 top-0 h-6 bg-gradient-to-b from-white to-transparent" />
                          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-6 bg-gradient-to-t from-white to-transparent" />
                          <div className="grid grid-cols-3 divide-x divide-blue-100 px-2">
                            {/* Hours */}
                            <div className="h-48 overflow-y-auto snap-y snap-mandatory py-3">
                              {[...Array(12)].map((_, i) => {
                                const val = i + 1;
                                const selected = timePicker.customHour === val;
                                return (
                                  <div
                                    key={val}
                                    onClick={() => setTimePicker((prev) => ({ ...prev, customHour: val }))}
                                    className={`h-12 flex items-center justify-center snap-center cursor-pointer transition-colors ${selected ? 'text-blue-700 font-semibold' : 'text-gray-700 hover:text-blue-600'}`}
                                  >
                                    <span className={`text-sm ${selected ? 'scale-105' : ''}`}>{val}</span>
                                  </div>
                                );
                              })}
                            </div>
                            {/* Minutes (step 5) */}
                            <div className="h-48 overflow-y-auto snap-y snap-mandatory py-3">
                              {[...Array(12)].map((_, i) => {
                                const val = i * 5;
                                const selected = (timePicker.customMinute ?? -1) === val;
                                return (
                                  <div
                                    key={val}
                                    onClick={() => setTimePicker((prev) => ({ ...prev, customMinute: val }))}
                                    className={`h-12 flex items-center justify-center snap-center cursor-pointer transition-colors ${selected ? 'text-blue-700 font-semibold' : 'text-gray-700 hover:text-blue-600'}`}
                                  >
                                    <span className={`tabular-nums text-sm ${selected ? 'scale-105' : ''}`}>{String(val).padStart(2, '0')}</span>
                                  </div>
                                );
                              })}
                            </div>
                            {/* AM/PM */}
                            <div className="h-48 overflow-y-auto snap-y snap-mandatory py-3">
                              {(['AM', 'PM'] as const).map((val) => {
                                const selected = timePicker.customMeridiem === val;
                                return (
                                  <div
                                    key={val}
                                    onClick={() => setTimePicker((prev) => ({ ...prev, customMeridiem: val }))}
                                    className={`h-12 flex items-center justify-center snap-center cursor-pointer transition-colors ${selected ? 'text-blue-700 font-semibold' : 'text-gray-700 hover:text-blue-600'}`}
                                  >
                                    <span className={`text-sm tracking-wide ${selected ? 'scale-105' : ''}`}>{val}</span>
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={handleCustomTimeSelection}
                      disabled={
                        !timePicker.customDate ||
                        (!timePicker.customTime &&
                          !(timePicker.customHour && timePicker.customMinute != null && timePicker.customMeridiem))
                      }
                      className="w-full px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                    >
                      ✅ Reschedule to custom time
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="flex space-x-3">
              <button
                onClick={closeTimePicker}
                className="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteEvent}
                className="flex-1 px-4 py-2 bg-red-100 hover:bg-red-200 text-red-800 rounded transition-colors"
                title="Delete this event permanently"
              >
                🗑️ Delete Event
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </motion.div>
  );
};

export default ConflictDetectionPanel;
