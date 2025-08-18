import React from 'react';
import { motion } from 'framer-motion';
import { MicrophoneIcon, SpeakerWaveIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import VoiceCommandCenter from '../../components/voice/VoiceCommandCenter';
import { useDashboard } from '../../hooks/useDashboard';
import { useVoice } from '../../hooks/useVoice';
import { useSystemHealth } from '../../hooks/useSystemHealth';
import { getPriorityLabel } from '../../utils/priorityUtils';

const VoicePage: React.FC = () => {
  const { events, loadDashboardData } = useDashboard();
  const { isListening, isProcessing, transcript } = useVoice();
  const { isVoiceHealthy } = useSystemHealth();

  // Get recent voice commands (last 5 voice-created events)
  const recentVoiceCommands = events
    .filter(event => event.created_via === 'voice')
    .sort((a, b) => new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime())
    .slice(0, 5);

  const getStatusColor = () => {
    if (isListening) return 'text-red-500';
    if (isProcessing) return 'text-yellow-500';
    if (isVoiceHealthy) return 'text-green-500';
    return 'text-gray-400';
  };

  const getStatusText = () => {
    if (isListening) return 'Listening...';
    if (isProcessing) return 'Processing...';
    if (isVoiceHealthy) return 'Ready';
    return 'Offline';
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div 
        className="text-center mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center justify-center">
          <MicrophoneIcon className="h-8 w-8 mr-3 text-blue-500" />
          Voice Hub
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Create events using natural voice commands powered by AI. Speak naturally and watch your calendar update automatically.
        </p>
      </motion.div>

      {/* Voice Status Indicator */}
      <motion.div
        className="bg-white rounded-xl p-4 shadow-sm border border-gray-200 mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded-full ${
              isListening ? 'bg-red-500 animate-pulse' :
              isProcessing ? 'bg-yellow-500 animate-pulse' :
              isVoiceHealthy ? 'bg-green-500' : 'bg-gray-400'
            }`}></div>
            <span className={`font-medium ${getStatusColor()}`}>
              Voice Status: {getStatusText()}
            </span>
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center space-x-1">
              <SpeakerWaveIcon className="h-4 w-4" />
              <span>BERT AI: 87% Accuracy</span>
            </div>
            <div className="flex items-center space-x-1">
              <CheckCircleIcon className="h-4 w-4 text-green-500" />
              <span>Browser Supported</span>
            </div>
          </div>
        </div>

        {/* Current Transcript Display */}
        {transcript && (
          <div className="mt-3 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
            <p className="text-sm text-blue-800">
              <strong>Current Transcript:</strong> "{transcript}"
            </p>
          </div>
        )}
      </motion.div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main Voice Command Center */}
        <motion.div 
          className="lg:col-span-2"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <VoiceCommandCenter onEventCreated={loadDashboardData} />
        </motion.div>

        {/* Recent Voice Commands */}
        <motion.div
          className="lg:col-span-1"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 h-fit">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              🗣️ Recent Voice Commands
            </h3>
            
            {recentVoiceCommands.length > 0 ? (
              <div className="space-y-3">
                {recentVoiceCommands.map((event, index) => (
                  <div 
                    key={event.id || index}
                    className="p-3 bg-gray-50 rounded-lg border border-gray-100 hover:border-gray-200 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="text-sm font-medium text-gray-900 mb-1">
                          {event.title}
                        </h4>
                        {event.description && !event.description.toLowerCase().includes('created via voice') && (
                          <p className="text-xs text-gray-600 mb-2">
                            {event.description.length > 60 
                              ? `${event.description.substring(0, 60)}...`
                              : event.description
                            }
                          </p>
                        )}
                        <div className="flex items-center space-x-2 text-xs text-gray-500">
                          <MicrophoneIcon className="h-3 w-3" />
                          <span>Voice Created</span>
                          {event.priority_level && (
                            <>
                              <span>•</span>
                              {(() => {
                                const { label: priorityLabel, color: priorityColor } = getPriorityLabel(event.priority_level || 3);
                                const bgColor = {
                                  red: 'bg-red-100 text-red-800',
                                  orange: 'bg-orange-100 text-orange-800',
                                  yellow: 'bg-yellow-100 text-yellow-800', 
                                  green: 'bg-green-100 text-green-800',
                                  gray: 'bg-gray-100 text-gray-800'
                                }[priorityColor];
                                
                                return (
                                  <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${bgColor}`}>
                                    {priorityLabel}
                                  </span>
                                );
                              })()}
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <MicrophoneIcon className="h-12 w-12 mx-auto mb-3 text-gray-300" />
                <p className="text-sm">No voice commands yet</p>
                <p className="text-xs mt-1">
                  Start by clicking the microphone button to create your first voice event!
                </p>
              </div>
            )}
          </div>

          {/* Voice Tips */}
          <div className="bg-blue-50 rounded-xl p-4 mt-4 border border-blue-100">
            <h4 className="text-sm font-semibold text-blue-900 mb-2">
              💡 Voice Tips
            </h4>
            <ul className="text-xs text-blue-800 space-y-1">
              <li>• Speak clearly and naturally</li>
              <li>• Include time, date, and details</li>
              <li>• Try: "Meeting tomorrow at 3pm"</li>
              <li>• AI detects priority automatically</li>
            </ul>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default VoicePage;
