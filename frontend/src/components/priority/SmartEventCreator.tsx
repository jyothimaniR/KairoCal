import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { PlusIcon } from '@heroicons/react/24/outline';
import ConflictResolver from './ConflictResolver';
import { apiService } from '../../services/apiService';

interface EventFormData {
  title: string;
  description: string;
  start_time: string;
  end_time: string;
  location?: string;
}

const SmartEventCreator: React.FC = () => {
  const [formData, setFormData] = useState<EventFormData>({
    title: '',
    description: '',
    start_time: '',
    end_time: '',
    location: ''
  });
  
  const [showConflictResolver, setShowConflictResolver] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [created, setCreated] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title || !formData.start_time || !formData.end_time) {
      alert('Please fill in all required fields');
      return;
    }

    // Show conflict resolver first
    setShowConflictResolver(true);
  };

  const handleConflictResolved = async () => {
    try {
      setIsCreating(true);
      setShowConflictResolver(false);

      // Create the event
      const eventData = {
        ...formData,
        priority_level: 3, // Default priority
        created_via: 'manual'
      };

      await apiService.createEvent(eventData, 'frontend-test-user');
      
      setCreated(true);
      
      // Reset form after 2 seconds
      setTimeout(() => {
        setCreated(false);
        setFormData({
          title: '',
          description: '',
          start_time: '',
          end_time: '',
          location: ''
        });
      }, 2000);

    } catch (error) {
      console.error('Error creating event:', error);
      alert('Failed to create event. Please try again.');
    } finally {
      setIsCreating(false);
    }
  };

  const handleCancel = () => {
    setShowConflictResolver(false);
  };

  const generateSampleData = () => {
    const now = new Date();
    const startTime = new Date(now.getTime() + 2 * 60 * 60 * 1000); // 2 hours from now
    const endTime = new Date(startTime.getTime() + 60 * 60 * 1000); // 1 hour duration

    setFormData({
      title: 'Important Strategy Meeting',
      description: 'Quarterly planning session with leadership team',
      start_time: startTime.toISOString().slice(0, 16), // YYYY-MM-DDTHH:MM format
      end_time: endTime.toISOString().slice(0, 16),
      location: 'Conference Room A'
    });
  };

  const generateConflictingData = () => {
    const conflictTime = new Date('2025-08-17T10:30:00');
    const endTime = new Date('2025-08-17T11:30:00');

    setFormData({
      title: 'New Meeting (Conflict Test)',
      description: 'This will conflict with existing 10:00 AM events',
      start_time: conflictTime.toISOString().slice(0, 16),
      end_time: endTime.toISOString().slice(0, 16),
      location: 'Office'
    });
  };

  if (showConflictResolver) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ConflictResolver
          eventData={{
            title: formData.title,
            start_time: formData.start_time + ':00', // Add seconds
            end_time: formData.end_time + ':00',
            description: formData.description
          }}
          onResolved={handleConflictResolved}
          onCancel={handleCancel}
        />
      </div>
    );
  }

  if (created) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="min-h-screen bg-green-50 flex items-center justify-center"
      >
        <div className="bg-white p-8 rounded-lg shadow-lg text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Event Created Successfully!</h2>
          <p className="text-gray-600">Your event "{formData.title}" has been scheduled.</p>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-lg overflow-hidden"
        >
          {/* Header */}
          <div className="bg-blue-600 p-6 text-white">
            <div className="flex items-center">
              <PlusIcon className="h-8 w-8 mr-3" />
              <div>
                <h1 className="text-2xl font-bold">Smart Event Creator</h1>
                <p className="text-blue-100 mt-1">AI-powered conflict detection and priority scheduling</p>
              </div>
            </div>
          </div>

          {/* Test Buttons */}
          <div className="p-6 border-b border-gray-200 bg-gray-50">
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={generateSampleData}
                className="px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700"
              >
                Fill Sample Data
              </button>
              <button
                type="button"
                onClick={generateConflictingData}
                className="px-4 py-2 bg-orange-600 text-white text-sm rounded-md hover:bg-orange-700"
              >
                Generate Conflict Test
              </button>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Use "Generate Conflict Test" to test the conflict detection with the 10:00 AM events.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6">
            <div className="space-y-6">
              {/* Title */}
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                  Event Title *
                </label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter event title"
                />
              </div>

              {/* Description */}
              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter event description"
                />
              </div>

              {/* Date and Time */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="start_time" className="block text-sm font-medium text-gray-700 mb-2">
                    Start Time *
                  </label>
                  <input
                    type="datetime-local"
                    id="start_time"
                    name="start_time"
                    value={formData.start_time}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label htmlFor="end_time" className="block text-sm font-medium text-gray-700 mb-2">
                    End Time *
                  </label>
                  <input
                    type="datetime-local"
                    id="end_time"
                    name="end_time"
                    value={formData.end_time}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Location */}
              <div>
                <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
                  Location
                </label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter location"
                />
              </div>
            </div>

            {/* Submit Button */}
            <div className="mt-8">
              <button
                type="submit"
                disabled={isCreating}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                {isCreating ? (
                  <>
                    <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2 inline-block"></span>
                    Creating Event...
                  </>
                ) : (
                  'Create Event with AI Conflict Detection'
                )}
              </button>
            </div>

            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">
                ✨ AI will automatically detect conflicts and suggest optimal scheduling
              </p>
            </div>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default SmartEventCreator;
