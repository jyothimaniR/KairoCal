import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';

interface ConflictEvent {
  id: string;
  title: string;
  start_time: string;
  end_time: string;
  priority_level: number;
  description?: string;
}

interface DetectedConflict {
  id: string;
  timeSlot: string;
  events: ConflictEvent[];
  severity: 'low' | 'medium' | 'high';
  suggestedResolution: string;
  bertAnalysis?: {
    confidence: number;
    reasoning: string;
  };
}

interface TimeSlotSuggestion {
  date: string;
  time: string;
  display: string;
  available: boolean;
}

const PRIORITY_LEVELS = [
  { value: 1, label: '1 - Very Low', confidence: 0 },
  { value: 2, label: '2 - Low', confidence: 0 },
  { value: 3, label: '3 - Medium', confidence: 0 },
  { value: 4, label: '4 - High', confidence: 0 },
  { value: 5, label: '5 - Critical', confidence: 0 }
];

const PriorityConflictResolver: React.FC = () => {
  const [conflicts, setConflicts] = useState<DetectedConflict[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedEventToReschedule, setSelectedEventToReschedule] = useState<string | null>(null);
  const [showTimeSlots, setShowTimeSlots] = useState(false);
  const [suggestedSlots, setSuggestedSlots] = useState<TimeSlotSuggestion[]>([]);
  const [customDate, setCustomDate] = useState('');
  const [customTime, setCustomTime] = useState('');
  const [isRescheduling, setIsRescheduling] = useState(false);
  const [deleteModal, setDeleteModal] = useState<{show: boolean, event: ConflictEvent | null}>({
    show: false,
    event: null
  });

  useEffect(() => {
    detectConflicts();
  }, []);

  const detectConflicts = async () => {
    try {
      setIsLoading(true);
      console.log('🔍 PriorityConflictResolver: Starting improved conflict detection...');
      
      // Get all events
      const events = await apiService.getEvents();
      console.log(`📊 Retrieved ${events.length} events`);

      if (events.length < 2) {
        console.log('⚠️ Not enough events to detect conflicts');
        setConflicts([]);
        return;
      }

      // 🔧 MAJOR FIX: Use client-side conflict detection to avoid duplicates
      // This ensures each conflict pair is detected only once
      const allDetectedConflicts: DetectedConflict[] = [];
      const timeEvents = events.filter(event => {
        const isAllDay = (event as any).is_all_day || (event as any).all_day || false;
        if (isAllDay) {
          console.log(`📅 Skipping all-day event: ${event.title}`);
          return false;
        }
        return true;
      });

      console.log(`⏰ Checking ${timeEvents.length} time-based events for conflicts`);

      // Check for overlapping events using proper pairwise comparison
      const conflictPairs: Array<[any, any]> = [];
      
      for (let i = 0; i < timeEvents.length; i++) {
        for (let j = i + 1; j < timeEvents.length; j++) {
          const event1 = timeEvents[i];
          const event2 = timeEvents[j];
          
          const start1 = new Date(event1.start_time);
          const end1 = new Date(event1.end_time);
          const start2 = new Date(event2.start_time);  
          const end2 = new Date(event2.end_time);
          
          console.log(`🔄 Checking overlap: "${event1.title}" vs "${event2.title}"`);
          console.log(`   Event 1: ${start1.toLocaleString()} - ${end1.toLocaleString()}`);
          console.log(`   Event 2: ${start2.toLocaleString()} - ${end2.toLocaleString()}`);
          
          // Check for time overlap: events overlap if start1 < end2 AND start2 < end1
          const hasOverlap = start1 < end2 && start2 < end1;
          
          console.log(`   Result: ${hasOverlap ? '🚨 CONFLICT DETECTED!' : '✅ No conflict'}`);
          
          if (hasOverlap) {
            conflictPairs.push([event1, event2]);
            console.log(`🆕 Added conflict pair: ${event1.title} vs ${event2.title}`);
          }
        }
      }

      console.log(`🗂️ Found ${conflictPairs.length} unique conflict pairs`);

      // Convert conflict pairs to DetectedConflict objects
      conflictPairs.forEach(([event1, event2]) => {
        // Calculate overlap details
        const start1 = new Date(event1.start_time);
        const end1 = new Date(event1.end_time);
        const start2 = new Date(event2.start_time);
        const end2 = new Date(event2.end_time);
        
        const overlapStart = new Date(Math.max(start1.getTime(), start2.getTime()));
        const overlapEnd = new Date(Math.min(end1.getTime(), end2.getTime()));
        const overlapMinutes = Math.round((overlapEnd.getTime() - overlapStart.getTime()) / (1000 * 60));
        
        // Use the earlier event's start time as the conflict time slot
        const conflictTimeSlot = start1 <= start2 ? event1.start_time : event2.start_time;
        
        // Create unique conflict ID based on event IDs (sorted for consistency)
        const eventIds = [event1.id, event2.id].sort();
        const conflictId = `conflict-${eventIds.join('-')}`;
        
        // Determine severity based on overlap duration and priorities
        let severity: 'low' | 'medium' | 'high' = 'medium';
        const priority1 = event1.priority_level || 3;
        const priority2 = event2.priority_level || 3;
        const highestPriority = Math.max(priority1, priority2); // Higher number = higher priority
        
        if (overlapMinutes >= 60 || highestPriority <= 2) {
          severity = 'high';
        } else if (overlapMinutes >= 30 || highestPriority <= 3) {
          severity = 'medium';
        } else {
          severity = 'low';
        }
        
        const detectedConflict: DetectedConflict = {
          id: conflictId,
          timeSlot: conflictTimeSlot,
          events: [
            {
              id: event1.id || 'unknown',
              title: event1.title,
              start_time: event1.start_time,
              end_time: event1.end_time,
              priority_level: priority1,
              description: event1.description
            },
            {
              id: event2.id || 'unknown',
              title: event2.title,
              start_time: event2.start_time,
              end_time: event2.end_time,
              priority_level: priority2,
              description: event2.description
            }
          ],
          severity,
          suggestedResolution: `${overlapMinutes} minute overlap detected. Consider rescheduling one event.`,
          bertAnalysis: {
            confidence: 0.95,
            reasoning: `Time overlap analysis: ${overlapMinutes} minutes overlap between "${event1.title}" and "${event2.title}"`
          }
        };
        
        allDetectedConflicts.push(detectedConflict);
        console.log(`✅ Created conflict: ${event1.title} vs ${event2.title} (${overlapMinutes}min overlap)`);
      });

      console.log(`🎯 Total unique conflicts detected: ${allDetectedConflicts.length}`);
      setConflicts(allDetectedConflicts);

    } catch (error) {
      console.error('❌ Error in conflict detection:', error);
      setConflicts([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Generate smart AI recommendation based on priority analysis
  const generateAIRecommendation = (conflict: DetectedConflict) => {
    const events = conflict.events;
    if (events.length !== 2) return "Consider rescheduling one of the conflicting events.";
    
    const [event1, event2] = events;
    const priority1 = event1.priority_level || 3;
    const priority2 = event2.priority_level || 3;
    
    // Priority recommendations (higher number = higher priority in KairoCal)
    // FIXED: Corrected the logic - we should move the LOWER priority event (lower number)
    if (priority1 < priority2) {
      // Event1 has lower priority (lower number), so move it
      return `Consider moving "${event1.title}" (Priority ${priority1} - ${getPriorityLabel(priority1)}).`;
    } else if (priority2 < priority1) {
      // Event2 has lower priority (lower number), so move it
      return `Consider moving "${event2.title}" (Priority ${priority2} - ${getPriorityLabel(priority2)}).`;
    } else {
      // Same priority - suggest based on event characteristics
      const duration1 = new Date(event1.end_time).getTime() - new Date(event1.start_time).getTime();
      const duration2 = new Date(event2.end_time).getTime() - new Date(event2.start_time).getTime();
      
      if (duration1 > duration2) {
        return `Consider moving "${event2.title}" (shorter duration).`;
      } else {
        return `Consider moving "${event1.title}" (shorter duration).`;
      }
    }
  };

  // Helper function to get priority label
  const getPriorityLabel = (priority: number): string => {
    const labels: Record<number, string> = {
      1: 'Very Low',
      2: 'Low', 
      3: 'Medium',
      4: 'High',
      5: 'Critical'
    };
    return labels[priority] || 'Unknown';
  };

  const updateEventPriority = async (eventId: string, newPriority: number) => {
    try {
      console.log(`🔧 Updating event ${eventId} priority to ${newPriority}`);
      
      // Use the new conflicts API endpoint for priority updates
      const response = await fetch(`http://127.0.0.1:8000/api/v1/conflicts/event/${eventId}/priority?cognito_sub=frontend-test-user&new_priority=${newPriority}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('✅ Priority updated successfully:', result);
        
        // Refresh conflicts to show updated priorities
        await detectConflicts();
      } else {
        console.error('❌ Failed to update priority:', response.status, response.statusText);
        const errorData = await response.json().catch(() => ({}));
        console.error('Error details:', errorData);
      }
    } catch (error) {
      console.error('❌ Error updating priority:', error);
    }
  };

  const handleDeleteEvent = async (eventId: string) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/events/${eventId}?cognito_sub=frontend-test-user`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        // Close modal and refresh conflicts
        setDeleteModal({ show: false, event: null });
        await detectConflicts();
      } else {
        console.error('Failed to delete event');
      }
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  };

  const openDeleteModal = (event: ConflictEvent) => {
    setDeleteModal({ show: true, event });
  };

  const generateTimeSlots = async (eventToReschedule: ConflictEvent) => {
    const slots: TimeSlotSuggestion[] = [];
    const today = new Date();
    const baseTime = new Date(eventToReschedule.start_time);
    const eventDuration = new Date(eventToReschedule.end_time).getTime() - baseTime.getTime();
    const eventDurationMinutes = Math.floor(eventDuration / (1000 * 60));
    
    // TIMEZONE FIX: Helper function to create local time without automatic UTC conversion
    const createLocalTime = (date: Date, hour: number) => {
      return new Date(date.getFullYear(), date.getMonth(), date.getDate(), hour, 0, 0, 0);
    };
    
    // Get all existing events to check for conflicts
    let existingEvents: any[] = [];
    try {
      existingEvents = await apiService.getEvents();
    } catch (error) {
      console.error('Error fetching events for slot checking:', error);
    }
    
    // Function to check if a time slot is available
    const isSlotAvailable = (slotStart: Date, slotEnd: Date) => {
      return !existingEvents.some(event => {
        if (event.id === eventToReschedule.id) return false; // Don't conflict with itself
        
        const eventStart = new Date(event.start_time);
        const eventEnd = new Date(event.end_time);
        
        // Check for any overlap
        return (slotStart < eventEnd && slotEnd > eventStart);
      });
    };
    
    // Determine which dates to suggest based on conflict date
    const conflictDate = new Date(baseTime);
    const datesToSuggest = [];
    
    // If conflict is today, suggest later today + tomorrow + next few days
    if (conflictDate.toDateString() === today.toDateString()) {
      datesToSuggest.push(
        { date: new Date(today), label: 'Today', hours: [14, 16, 19, 21] },
        { date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1), label: 'Tomorrow', hours: [9, 11, 14, 16, 19] }
      );
    }
    // If conflict is tomorrow, suggest tomorrow + day after
    else if (conflictDate.toDateString() === new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1).toDateString()) {
      datesToSuggest.push(
        { date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1), label: 'Tomorrow', hours: [9, 11, 14, 16, 19] },
        { date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 2), label: 'Day After', hours: [9, 11, 14, 16, 19] }
      );
    }
    // If conflict is in the future, suggest same day (different times) + next day
    else {
      datesToSuggest.push(
        { date: new Date(conflictDate), label: formatDate(conflictDate.toISOString()), hours: [9, 11, 14, 16, 19, 21] },
        { date: new Date(conflictDate.getFullYear(), conflictDate.getMonth(), conflictDate.getDate() + 1), label: 'Next Day', hours: [9, 11, 14, 16, 19] }
      );
    }
    
    // Generate slots for each date
    for (const dateOption of datesToSuggest) {
      for (const hour of dateOption.hours) {
        const slotStart = createLocalTime(dateOption.date, hour);
        const slotEnd = new Date(slotStart.getTime() + eventDurationMinutes * 60 * 1000);
        
        // Only suggest future times
        if (slotStart > new Date()) {
          const isAvailable = isSlotAvailable(slotStart, slotEnd);
          
          slots.push({
            date: slotStart.getFullYear() + '-' + 
                  String(slotStart.getMonth() + 1).padStart(2, '0') + '-' + 
                  String(slotStart.getDate()).padStart(2, '0'),
            time: String(slotStart.getHours()).padStart(2, '0') + ':' + 
                  String(slotStart.getMinutes()).padStart(2, '0'),
            display: `${dateOption.label} ${hour > 12 ? hour - 12 : hour}:00 ${hour >= 12 ? 'PM' : 'AM'}`,
            available: isAvailable
          });
        }
      }
    }
    
    return slots;
  };

  const handleRescheduleClick = async (event: ConflictEvent) => {
    setSelectedEventToReschedule(event.id);
    setShowTimeSlots(true);
    
    // Generate time slots asynchronously to check availability
    try {
      const slots = await generateTimeSlots(event);
      setSuggestedSlots(slots);
    } catch (error) {
      console.error('Error generating time slots:', error);
      setSuggestedSlots([]);
    }
  };

  const rescheduleEvent = async (eventId: string, newDateTime: string) => {
    try {
      setIsRescheduling(true);
      
      // Find the event to get its duration
      const eventToReschedule = conflicts
        .flatMap(c => c.events)
        .find(e => e.id === eventId);
      
      if (!eventToReschedule) return;
      
      const originalStart = new Date(eventToReschedule.start_time);
      const originalEnd = new Date(eventToReschedule.end_time);
      const duration = originalEnd.getTime() - originalStart.getTime();
      
      // TIMEZONE FIX: Create date as local time, not UTC
      // This ensures the user's selected time is preserved without timezone conversion
      const [datePart, timePart] = newDateTime.split('T');
      const [year, month, day] = datePart.split('-').map(Number);
      const [hour, minute] = (timePart || '00:00').split(':').map(Number);
      
      // Create local time without letting JavaScript convert to UTC
      const newStart = new Date(year, month - 1, day, hour, minute);
      const newEnd = new Date(newStart.getTime() + duration);
      
      // CRITICAL FIX: Use local time formatting instead of toISOString() which converts to UTC
      const formatLocalDateTime = (date: Date): string => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
      };
      
      console.log(`🔧 TIMEZONE FIX - Input: ${newDateTime}, Local: ${newStart}, Duration: ${duration}ms`);
      
      const success = await apiService.rescheduleEvent(
        eventId,
        formatLocalDateTime(newStart),
        formatLocalDateTime(newEnd)
      );
      
      if (success) {
        setShowTimeSlots(false);
        setSelectedEventToReschedule(null);
        await detectConflicts(); // Refresh conflicts
      }
    } catch (error) {
      console.error('Error rescheduling event:', error);
    } finally {
      setIsRescheduling(false);
    }
  };

  const handleCustomReschedule = async () => {
    if (!selectedEventToReschedule || !customDate || !customTime) return;
    
    const newDateTime = `${customDate}T${customTime}:00`;
    await rescheduleEvent(selectedEventToReschedule, newDateTime);
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    if (date.toDateString() === today.toDateString()) return 'Today';
    if (date.toDateString() === tomorrow.toDateString()) return 'Tomorrow';
    
    const nextMonday = new Date(today);
    nextMonday.setDate(today.getDate() + (1 + 7 - today.getDay()) % 7);
    if (date.toDateString() === nextMonday.toDateString()) return 'Monday';
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          <span className="ml-3 text-gray-600">Analyzing conflicts...</span>
        </div>
      </div>
    );
  }

  if (conflicts.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="text-center py-8">
          <div className="text-green-500 text-4xl mb-4">✅</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Conflicts Detected</h3>
          <p className="text-gray-600">Your schedule is well-organized!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {conflicts.map((conflict) => (
        <motion.div
          key={conflict.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-sm border border-red-200 p-6"
        >
          {/* Conflict Header */}
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-red-100 rounded-lg">
              <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-red-800">
                🚨 CONFLICT DETECTED on {formatDate(conflict.timeSlot)} at {formatTime(conflict.timeSlot)}
              </h3>
              <p className="text-sm text-red-600">Choose which event to reschedule:</p>
            </div>
          </div>

          {/* Conflicting Events */}
          <div className="space-y-4">
            {conflict.events.map((event, index) => (
              <div
                key={`${event.id}-${index}`}
                className="border border-gray-200 rounded-lg p-4 bg-gray-50"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-2">
                      {index === 0 ? '🍳' : '💼'} {event.title}
                    </h4>
                    
                    {/* Priority Dropdown */}
                    <div className="flex items-center space-x-2 mb-3">
                      <label className="text-sm text-gray-600">Priority:</label>
                      <select
                        value={event.priority_level}
                        onChange={(e) => updateEventPriority(event.id, parseInt(e.target.value))}
                        className="border border-gray-300 rounded px-2 py-1 text-sm"
                        title="Select priority level"
                      >
                        {PRIORITY_LEVELS.map((level) => (
                          <option key={level.value} value={level.value}>
                            {level.label}
                          </option>
                        ))}
                      </select>
                      <span className="text-xs text-gray-500">
                        {Math.round((conflict.bertAnalysis?.confidence || 0.9) * 100)}% confidence
                      </span>
                    </div>
                    
                    <p className="text-sm text-gray-600">
                      {formatTime(event.start_time)} - {formatTime(event.end_time)}
                    </p>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleRescheduleClick(event)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
                    >
                      Reschedule This Event
                    </button>
                    
                    <button
                      onClick={() => openDeleteModal(event)}
                      className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
                    >
                      Delete Event
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* AI Recommendation */}
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start space-x-2">
              <span className="text-blue-600 text-sm">🤖</span>
              <div className="text-sm text-blue-800">
                <strong>AI Recommendation:</strong> {generateAIRecommendation(conflict)}
              </div>
            </div>
          </div>
          
          {/* Conflict Details */}
          <div className="mt-2 p-3 bg-gray-50 border border-gray-200 rounded-lg">
            <div className="flex items-start space-x-2">
              <span className="text-gray-600 text-sm">ℹ️</span>
              <div className="text-sm text-gray-700">
                <strong>Conflict Details:</strong> {conflict.suggestedResolution}
              </div>
            </div>
          </div>
        </motion.div>
      ))}

      {/* Time Slot Selection Modal */}
      <AnimatePresence>
        {showTimeSlots && selectedEventToReschedule && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              className="bg-white rounded-xl shadow-xl p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-gray-900">
                  ⏰ Reschedule Event
                </h3>
                <button
                  onClick={() => setShowTimeSlots(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-6">
                {/* Smart Suggestions */}
                <div>
                  <h4 className="font-medium text-gray-900 mb-4">
                    🎯 Smart Suggestions (Priority-Based):
                  </h4>
                  
                  {/* Smart time slot suggestions */}
                  <div className="space-y-4">
                    {suggestedSlots.length === 0 ? (
                      <div className="text-center py-4 text-gray-500">
                        Loading available time slots...
                      </div>
                    ) : (
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                        {suggestedSlots.map((slot, index) => (
                          <button
                            key={index}
                            onClick={() => slot.available ? rescheduleEvent(selectedEventToReschedule, `${slot.date}T${slot.time}:00`) : null}
                            disabled={isRescheduling || !slot.available}
                            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                              slot.available 
                                ? 'bg-blue-100 hover:bg-blue-200 text-blue-800 cursor-pointer' 
                                : 'bg-red-100 text-red-600 cursor-not-allowed opacity-60'
                            }`}
                            title={slot.available ? 'Available slot' : 'Time slot already occupied'}
                          >
                            {slot.display}
                            {!slot.available && ' ❌'}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Custom Date & Time */}
                <div className="border-t pt-4">
                  <h5 className="font-medium text-gray-900 mb-3">📅 Custom Date & Time</h5>
                  <div className="flex items-center space-x-3">
                    <div>
                      <label className="block text-sm text-gray-600 mb-1">Date:</label>
                      <input
                        type="date"
                        value={customDate}
                        onChange={(e) => setCustomDate(e.target.value)}
                        className="border border-gray-300 rounded px-3 py-2 text-sm"
                        min={new Date().toISOString().split('T')[0]}
                        title="Select date"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-gray-600 mb-1">Time:</label>
                      <input
                        type="time"
                        value={customTime}
                        onChange={(e) => setCustomTime(e.target.value)}
                        className="border border-gray-300 rounded px-3 py-2 text-sm"
                        title="Select time"
                      />
                    </div>
                    <div className="pt-6">
                      <button
                        onClick={handleCustomReschedule}
                        disabled={!customDate || !customTime || isRescheduling}
                        className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg text-sm font-medium"
                      >
                        Schedule Custom Time
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {isRescheduling && (
                <div className="mt-4 text-center">
                  <div className="inline-flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                    <span className="text-sm text-gray-600">Rescheduling event...</span>
                  </div>
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Modern Delete Confirmation Modal */}
      <AnimatePresence>
        {deleteModal.show && deleteModal.event && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
            onClick={() => setDeleteModal({ show: false, event: null })}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-red-100 rounded-full">
                  <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Delete Event</h3>
                  <p className="text-sm text-gray-500">This action cannot be undone</p>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <div className="font-medium text-gray-900">{deleteModal.event.title}</div>
                <div className="text-sm text-gray-600 mt-1">
                  {formatTime(deleteModal.event.start_time)} - {formatTime(deleteModal.event.end_time)}
                </div>
                {deleteModal.event.description && (
                  <div className="text-sm text-gray-500 mt-2">{deleteModal.event.description}</div>
                )}
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={() => setDeleteModal({ show: false, event: null })}
                  className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={() => handleDeleteEvent(deleteModal.event!.id)}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Delete Event
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default PriorityConflictResolver;
