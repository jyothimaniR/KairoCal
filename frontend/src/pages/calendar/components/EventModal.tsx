import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  XMarkIcon,
  CalendarDaysIcon,
  ClockIcon,
  MapPinIcon,
  DocumentTextIcon,
  StarIcon,
  MicrophoneIcon,
  PencilIcon,
  TrashIcon,
} from '@heroicons/react/24/outline';
import { CheckIcon } from '@heroicons/react/24/solid';
import ConflictWarning, { type ConflictInfo } from './ConflictWarning';
import type { Event } from '../../../services/apiService';
import { apiService } from '../../../services/apiService';
// Priority utilities imported but not used in this component

export interface EventModalProps {
  isOpen: boolean;
  onClose: () => void;
  event?: Event | null; // null for new event, Event for editing
  initialDate?: Date;
  initialStartTime?: Date;
  initialEndTime?: Date;
  onSave: (eventData: Partial<Event>) => Promise<boolean>;
  onDelete?: (eventId: string) => Promise<boolean>;
}

interface EventFormData {
  title: string;
  description: string;
  location: string;
  start_time: string; // ISO string
  end_time: string; // ISO string
  priority_level: number;
  all_day: boolean;
}

const PRIORITY_OPTIONS = [
  { value: 5, label: 'Critical', color: 'red', description: 'Urgent and important' },
  { value: 4, label: 'High', color: 'orange', description: 'Important tasks' },
  { value: 3, label: 'Medium', color: 'blue', description: 'Regular tasks' },
  { value: 2, label: 'Low', color: 'green', description: 'Nice to have' },
  { value: 1, label: 'Very Low', color: 'gray', description: 'Optional' },
];

const formatDateTimeLocal = (date: Date): string => {
  // Format date for datetime-local input (YYYY-MM-DDTHH:mm)
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};

const EventModal: React.FC<EventModalProps> = ({
  isOpen,
  onClose,
  event,
  initialDate,
  initialStartTime,
  initialEndTime,
  onSave,
  onDelete,
}) => {
  const [formData, setFormData] = useState<EventFormData>({
    title: '',
    description: '',
    location: '',
    start_time: '',
    end_time: '',
    priority_level: 3,
    all_day: false,
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [conflicts, setConflicts] = useState<ConflictInfo[]>([]);
  const [showConflicts, setShowConflicts] = useState(false);

  const isEditing = !!event;
  const modalTitle = isEditing ? 'Edit Event' : 'Create New Event';

  // Initialize form data
  useEffect(() => {
    if (isOpen) {
      if (event) {
        // Editing existing event
        setFormData({
          title: event.title,
          description: event.description || '',
          location: event.location || '',
          start_time: formatDateTimeLocal(new Date(event.start_time)),
          end_time: formatDateTimeLocal(new Date(event.end_time)),
          priority_level: event.priority_level || 3,
          all_day: event.all_day || event.is_all_day || false,
        });
      } else {
        // Creating new event
        const now = new Date();
        const startTime = initialStartTime || initialDate || now;
        const endTime = initialEndTime || new Date(startTime.getTime() + 60 * 60 * 1000); // 1 hour later
        
        setFormData({
          title: '',
          description: '',
          location: '',
          start_time: formatDateTimeLocal(startTime),
          end_time: formatDateTimeLocal(endTime),
          priority_level: 3,
          all_day: false,
        });
      }
      
      setErrors({});
      setShowDeleteConfirm(false);
    }
  }, [isOpen, event, initialDate, initialStartTime, initialEndTime]);

  const handleInputChange = (field: keyof EventFormData, value: string | number | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: '',
      }));
    }
    
    // Check for conflicts when time changes
    if (field === 'start_time' || field === 'end_time') {
      checkForConflicts();
    }
  };

  const checkForConflicts = async () => {
    if (!formData.title || !formData.start_time || !formData.end_time) {
      return;
    }

    try {
      const conflictData = await apiService.conflictsCheck({
        title: formData.title,
        start_time: new Date(formData.start_time).toISOString(),
        end_time: new Date(formData.end_time).toISOString(),
        description: formData.description,
        location: formData.location,
        is_all_day: formData.all_day,
      });

      if (conflictData && conflictData.conflicts && conflictData.conflicts.length > 0) {
        const mappedConflicts: ConflictInfo[] = conflictData.conflicts.map((conflict: any) => ({
          type: conflict.type || 'overlap',
          severity: conflict.severity || 'medium',
          conflictingEvents: conflict.conflicting_events || [],
          message: conflict.message || 'Schedule conflict detected',
          suggestion: conflict.suggestion,
          confidence: conflict.confidence,
        }));
        
        setConflicts(mappedConflicts);
        setShowConflicts(true);
      } else {
        setConflicts([]);
        setShowConflicts(false);
      }
    } catch (error) {
      console.error('Error checking conflicts:', error);
      // Don't show conflicts on error to avoid blocking user
    }
  };

  const validateForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};
    
    if (!formData.title.trim()) {
      newErrors.title = 'Event title is required';
    }
    
    if (!formData.start_time) {
      newErrors.start_time = 'Start time is required';
    }
    
    if (!formData.end_time) {
      newErrors.end_time = 'End time is required';
    }
    
    if (formData.start_time && formData.end_time && !formData.all_day) {
      const startDate = new Date(formData.start_time);
      const endDate = new Date(formData.end_time);
      
      if (endDate <= startDate) {
        newErrors.end_time = 'End time must be after start time';
      }
    }
    
    // For all-day events, we don't need to validate end time vs start time
    // since they should be on the same day
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // Format dates for backend WITHOUT timezone conversion to prevent 1-hour offset bug
      const formatForBackend = (dateTimeString: string, isAllDay: boolean): string => {
        if (isAllDay) {
          // For all-day events, treat as UTC to prevent timezone issues
          const date = new Date(dateTimeString + 'Z');
          return date.toISOString();
        } else {
          // For timed events, preserve exact local time without timezone conversion
          const date = new Date(dateTimeString);
          const year = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const day = String(date.getDate()).padStart(2, '0');
          const hours = String(date.getHours()).padStart(2, '0');
          const minutes = String(date.getMinutes()).padStart(2, '0');
          const seconds = String(date.getSeconds()).padStart(2, '0');
          
          return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
        }
      };
      
      const eventData: Partial<Event> = {
        title: formData.title.trim(),
        description: formData.description.trim(), // Save empty string if cleared
        location: formData.location.trim(), // Save empty string if cleared
        start_time: formatForBackend(formData.start_time, formData.all_day),
        end_time: formatForBackend(formData.end_time, formData.all_day),
        priority_level: formData.priority_level,
        all_day: formData.all_day,
      };
      
      console.log('💾 Saving event with data:', eventData);
      console.log('📅 Form start time:', formData.start_time, '->', eventData.start_time);
      console.log('📅 Form end time:', formData.end_time, '->', eventData.end_time);
      console.log('🔄 All day:', formData.all_day);
      
      const success = await onSave(eventData);
      
      if (success) {
        onClose();
      }
    } catch (error) {
      console.error('Error saving event:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!event?.id || !onDelete) return;
    
    setIsSubmitting(true);
    
    try {
      const success = await onDelete(event.id);
      
      if (success) {
        onClose();
      }
    } catch (error) {
      console.error('Error deleting event:', error);
    } finally {
      setIsSubmitting(false);
      setShowDeleteConfirm(false);
    }
  };

  const handleAllDayChange = (allDay: boolean) => {
    if (allDay) {
      // Set to full day times - same day from 00:00:00 to 23:59:59
      const currentDate = formData.start_time.split('T')[0]; // Get just the date part
      
      setFormData(prev => ({
        ...prev,
        all_day: true,
        start_time: currentDate + 'T00:00:00',
        end_time: currentDate + 'T23:59:59',
      }));
    } else {
      setFormData(prev => ({ ...prev, all_day: false }));
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="bg-white rounded-xl shadow-2xl w-full max-w-3xl max-h-[95vh] overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <CalendarDaysIcon className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">{modalTitle}</h2>
                  {event?.created_via && (
                    <div className="flex items-center space-x-1 text-xs text-gray-500">
                      {event.created_via === 'voice' ? (
                        <MicrophoneIcon className="h-3 w-3" />
                      ) : (
                        <PencilIcon className="h-3 w-3" />
                      )}
                      <span>Created via {event.created_via}</span>
                    </div>
                  )}
                </div>
              </div>
              
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
                aria-label="Close modal"
              >
                <XMarkIcon className="h-5 w-5 text-gray-500" />
              </button>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6 space-y-6 overflow-y-auto max-h-[calc(95vh-180px)]">
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Event Title *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                placeholder="Enter event title..."
                className={`
                  w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                  ${errors.title ? 'border-red-300' : 'border-gray-300'}
                `}
              />
              {errors.title && (
                <p className="mt-1 text-sm text-red-600">{errors.title}</p>
              )}
            </div>

            {/* All Day Toggle */}
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="all-day"
                checked={formData.all_day}
                onChange={(e) => handleAllDayChange(e.target.checked)}
                className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
              />
              <label htmlFor="all-day" className="text-sm font-medium text-gray-700">
                All day event
              </label>
            </div>

            {/* Date and Time */}
            {formData.all_day ? (
              // All-day event: Single date field
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <ClockIcon className="inline h-4 w-4 mr-1" />
                  Event Date *
                </label>
                <input
                  type="date"
                  value={formData.start_time.split('T')[0]}
                  onChange={(e) => {
                    const dateValue = e.target.value;
                    // For all-day events, use the exact date without timezone conversion
                    handleInputChange('start_time', dateValue + 'T00:00:00');
                    handleInputChange('end_time', dateValue + 'T23:59:59');
                  }}
                  className={`
                    w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                    ${errors.start_time ? 'border-red-300' : 'border-gray-300'}
                  `}
                  aria-label="Event date"
                />
                {errors.start_time && (
                  <p className="mt-1 text-sm text-red-600">{errors.start_time}</p>
                )}
              </div>
            ) : (
              // Timed event: Start and end date/time fields
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <ClockIcon className="inline h-4 w-4 mr-1" />
                    Start Date & Time *
                  </label>
                  <input
                    type="datetime-local"
                    value={formData.start_time}
                    onChange={(e) => handleInputChange('start_time', e.target.value)}
                    className={`
                      w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                      ${errors.start_time ? 'border-red-300' : 'border-gray-300'}
                    `}
                    aria-label="Event start date and time"
                  />
                  {errors.start_time && (
                    <p className="mt-1 text-sm text-red-600">{errors.start_time}</p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    End Date & Time *
                  </label>
                  <input
                    type="datetime-local"
                    value={formData.end_time}
                    onChange={(e) => handleInputChange('end_time', e.target.value)}
                    className={`
                      w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                      ${errors.end_time ? 'border-red-300' : 'border-gray-300'}
                    `}
                    aria-label="Event end date and time"
                  />
                  {errors.end_time && (
                    <p className="mt-1 text-sm text-red-600">{errors.end_time}</p>
                  )}
                </div>
              </div>
            )}

            {/* Priority */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <StarIcon className="inline h-4 w-4 mr-1" />
                Priority Level
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2">
                {PRIORITY_OPTIONS.map(option => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => handleInputChange('priority_level', option.value)}
                    className={`
                      p-3 border rounded-lg text-left transition-all
                      ${formData.priority_level === option.value
                        ? 'bg-blue-100 border-blue-300 ring-2 ring-blue-200'
                        : 'bg-white border-gray-200 hover:bg-gray-50'
                      }
                    `}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className={`
                        text-sm font-medium
                        ${formData.priority_level === option.value ? 'text-blue-800' : 'text-gray-700'}
                      `}>
                        {option.label}
                      </span>
                      {formData.priority_level === option.value && (
                        <CheckIcon className="h-4 w-4 text-blue-600" />
                      )}
                    </div>
                    <p className="text-xs text-gray-500">{option.description}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Location */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPinIcon className="inline h-4 w-4 mr-1" />
                Location
              </label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) => handleInputChange('location', e.target.value)}
                placeholder="Enter event location..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <DocumentTextIcon className="inline h-4 w-4 mr-1" />
                Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                placeholder="Enter event description..."
                rows={4}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              />
            </div>

            {/* Event Info (for editing) */}
            {event && (
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Event Information</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                  <div>
                    <span className="font-medium">Created:</span> {event.created_at ? new Date(event.created_at).toLocaleDateString() : 'Unknown'}
                  </div>
                  {event.updated_at && event.updated_at !== event.created_at && (
                    <div>
                      <span className="font-medium">Modified:</span> {new Date(event.updated_at).toLocaleDateString()}
                    </div>
                  )}
                  {event.priority_confidence && (
                    <div>
                      <span className="font-medium">AI Confidence:</span> {Math.round(event.priority_confidence * 100)}%
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Conflict Warnings */}
            {showConflicts && conflicts.length > 0 && (
              <ConflictWarning
                conflicts={conflicts}
                event={{
                  id: event?.id || 'new',
                  title: formData.title,
                  start_time: new Date(formData.start_time).toISOString(),
                  end_time: new Date(formData.end_time).toISOString(),
                  priority_level: formData.priority_level,
                } as Event}
                onResolve={(conflictType, resolution) => {
                  console.log('Conflict resolution:', conflictType, resolution);
                  if (resolution === 'ignore') {
                    setShowConflicts(false);
                  }
                  // TODO: Implement other resolution types
                }}
                onDismiss={() => setShowConflicts(false)}
              />
            )}
          </form>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                {isEditing && onDelete && (
                  <button
                    type="button"
                    onClick={() => setShowDeleteConfirm(true)}
                    disabled={isSubmitting}
                    className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                  >
                    <TrashIcon className="inline h-4 w-4 mr-1" />
                    Delete Event
                  </button>
                )}
              </div>
              
              <div className="flex items-center space-x-3">
                <button
                  type="button"
                  onClick={onClose}
                  disabled={isSubmitting}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={isSubmitting || !formData.title.trim()}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? 'Saving...' : (isEditing ? 'Save Changes' : 'Create Event')}
                </button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Delete Confirmation Modal */}
        <AnimatePresence>
          {showDeleteConfirm && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-60"
              onClick={() => setShowDeleteConfirm(false)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <TrashIcon className="h-5 w-5 text-red-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Delete Event</h3>
                </div>
                
                <p className="text-gray-600 mb-6">
                  Are you sure you want to delete "{event?.title}"? This action cannot be undone.
                </p>
                
                <div className="flex items-center justify-end space-x-3">
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    disabled={isSubmitting}
                    className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleDelete}
                    disabled={isSubmitting}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
                  >
                    {isSubmitting ? 'Deleting...' : 'Delete Event'}
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </AnimatePresence>
  );
};

export default EventModal;
