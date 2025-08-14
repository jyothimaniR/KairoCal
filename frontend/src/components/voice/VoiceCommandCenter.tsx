import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MicrophoneIcon, 
  StopIcon,
  SparklesIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { useVoice } from '../../hooks/useVoice';
import { apiService } from '../../services/apiService';

interface VoiceCommandCenterProps {
  onEventCreated?: () => void;
}

const VoiceCommandCenter: React.FC<VoiceCommandCenterProps> = ({ onEventCreated }) => {
  const { 
    isListening, 
    isProcessing, 
    transcript, 
    error, 
    lastResult,
    isSupported,
    startListening, 
    stopListening, 
    clearError,
    reset
  } = useVoice();

  const [showResults, setShowResults] = useState(false);
  const [createdEvent, setCreatedEvent] = useState<{ id: string; title: string; description?: string; priority_level?: number; created_via?: string } | null>(null);
  const [isCreatingEvent, setIsCreatingEvent] = useState(false);

  const handleVoiceCommand = async () => {
    if (isListening) {
      stopListening();
      return;
    }

    try {
      const result = await startListening();
      if (result) {
        setShowResults(true);
      }
    } catch (error) {
      console.error('Voice command failed:', error);
    }
  };

  const handleCreateEvent = async () => {
    if (!transcript || !lastResult) return;
    
    try {
      setIsCreatingEvent(true);
      
      // Use the voice-specific API endpoint
      const result = await apiService.createVoiceEvent(transcript, 'frontend-test-user');
      
      if (result.success && result.event_id) {
        // Create a display-friendly event object with safe typing
        const ed = result.event_data as Record<string, unknown>;
        const displayEvent = {
          id: result.event_id,
          title: typeof ed.title === 'string' ? ed.title : transcript,
          description:
            typeof ed.description === 'string'
              ? ed.description
              : `Created via voice: ${transcript}`,
          priority_level: typeof ed.priority_level === 'number' ? ed.priority_level : lastResult.priority,
          created_via: 'voice' as const
        };
        
        setCreatedEvent(displayEvent);
        onEventCreated?.();
        
        // Reset after successful creation
        reset();
        setShowResults(false);
        
        // Clear created event after 5 seconds
        setTimeout(() => setCreatedEvent(null), 5000);
      } else {
        console.error('Failed to create event:', result.message || 'Unknown error');
        alert(`Failed to create event: ${result.message || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Failed to create event:', error);
      alert(`Failed to create event: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsCreatingEvent(false);
    }
  };

  const handleDismiss = () => {
    reset();
    setShowResults(false);
    clearError();
  };

  if (!isSupported) {
    return (
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          🎤 Voice Command Center
        </h2>
        <div className="text-center py-8">
          <ExclamationTriangleIcon className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
          <p className="text-gray-600">
            Voice recognition is not supported in your browser.
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Please use Chrome, Edge, or Safari for voice features.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
        🎤 Voice Command Center
      </h2>
      
      <div className="flex items-center justify-between">
        <div className="flex-1 mr-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Example voice commands:
          </h3>
          <p className="text-sm text-gray-600 mb-1">"Meeting with CEO tomorrow at 2pm"</p>
          <p className="text-sm text-gray-600 mb-1">"Call mom this evening"</p>
          <p className="text-sm text-gray-600">"Review project proposal by Friday"</p>
        </div>
        
        <div className="text-center">
          <motion.button
            onClick={handleVoiceCommand}
            disabled={isProcessing}
            className={`w-24 h-24 rounded-full flex items-center justify-center text-white shadow-lg transition-all duration-200 ${
              isListening 
                ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                : isProcessing
                ? 'bg-yellow-500 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
            whileHover={{ scale: isProcessing ? 1 : 1.05 }}
            whileTap={{ scale: isProcessing ? 1 : 0.95 }}
          >
            {isProcessing ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              >
                <SparklesIcon className="h-10 w-10" />
              </motion.div>
            ) : isListening ? (
              <StopIcon className="h-10 w-10" />
            ) : (
              <MicrophoneIcon className="h-10 w-10" />
            )}
          </motion.button>
          
          <p className="text-sm text-gray-600 mt-3">
            {isListening 
              ? 'Listening...' 
              : isProcessing 
              ? 'Processing...' 
              : 'Click to speak'
            }
          </p>
        </div>
      </div>

      {/* Error Display */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg"
          >
            <div className="flex items-center justify-between">
              <p className="text-sm text-red-700">{error}</p>
              <button 
                onClick={clearError}
                className="text-red-500 hover:text-red-700 text-sm"
              >
                ✕
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Success Notification */}
      <AnimatePresence>
        {createdEvent && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-700 font-medium">✅ Event Created Successfully!</p>
                <p className="text-xs text-green-600 mt-1">"{createdEvent.title}"</p>
              </div>
              <button 
                onClick={() => setCreatedEvent(null)}
                className="text-green-500 hover:text-green-700 text-sm"
              >
                ✕
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results Display */}
      <AnimatePresence>
        {showResults && transcript && lastResult && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg"
          >
            <div className="space-y-3">
              <div>
                <h4 className="text-sm font-medium text-blue-900 mb-1">
                  🗣️ You said:
                </h4>
                <p className="text-sm text-blue-800 italic">"{transcript}"</p>
              </div>
              
              <div className="border-t border-blue-200 pt-3">
                <h4 className="text-sm font-medium text-blue-900 mb-2">
                  🤖 AI Analysis:
                </h4>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <span className="text-blue-700">Priority:</span>
                    <span className={`ml-2 px-2 py-1 rounded text-xs ${
                      lastResult.priority === 1 ? 'bg-red-100 text-red-800' :
                      lastResult.priority === 2 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {lastResult.priority === 1 ? 'HIGH' : 
                       lastResult.priority === 2 ? 'MEDIUM' : 'LOW'}
                    </span>
                  </div>
                  <div>
                    <span className="text-blue-700">Confidence:</span>
                    <span className="ml-2 font-medium">
                      {Math.round(lastResult.confidence * 100)}%
                    </span>
                  </div>
                </div>
                
                {lastResult.reasoning && (
                  <p className="text-xs text-blue-600 mt-2">
                    💡 {lastResult.reasoning}
                  </p>
                )}
              </div>

              <div className="flex space-x-2 pt-2">
                <button 
                  onClick={handleCreateEvent}
                  disabled={isCreatingEvent}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isCreatingEvent ? 'Creating...' : '✅ Create Event'}
                </button>
                <button 
                  onClick={handleDismiss}
                  className="px-4 py-2 bg-gray-200 text-gray-700 text-sm rounded-lg hover:bg-gray-300"
                >
                  ✕ Dismiss
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default VoiceCommandCenter;
