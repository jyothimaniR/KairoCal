import React, { useCallback, useState } from 'react';
import { 
  MicrophoneIcon, 
  PencilIcon, 
  SparklesIcon, 
  CheckCircleIcon,
  StopIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';
import { voiceService } from '../../services/voiceService';
import { getPriorityLabel } from '../../utils/priorityUtils';

interface UnifiedEventCreatorProps {
  onEventCreated?: () => void;
}

type InputMode = 'text' | 'voice';

const UnifiedEventCreator: React.FC<UnifiedEventCreatorProps> = ({ onEventCreated }) => {
  const [inputMode, setInputMode] = useState<InputMode>('text');
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<{
    priority: number;
    confidence: number;
    reasoning: string;
  } | null>(null);
  const [created, setCreated] = useState<{ id: string; title: string; method: string } | null>(null);

  const canSubmit = text.trim().length > 0 && !isAnalyzing && !isCreating && !isListening;

  // Voice Recognition Setup
  const recognition = React.useMemo(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';
      return recognition;
    }
    return null;
  }, []);

  const handleVoiceStart = useCallback(() => {
    if (!recognition) {
      setError('Voice recognition not supported in this browser');
      return;
    }

    setError(null);
    setIsListening(true);
    setInputMode('voice');

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setText(transcript);
      setIsListening(false);
    };

    recognition.onerror = () => {
      setError('Voice recognition failed. Please try again.');
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  }, [recognition]);

  const handleVoiceStop = useCallback(() => {
    if (recognition) {
      recognition.stop();
    }
    setIsListening(false);
  }, [recognition]);

  const handleAnalyze = useCallback(async () => {
    if (!text.trim()) return;
    setError(null);
    setAnalysis(null);
    setIsAnalyzing(true);
    try {
      const res = await voiceService.analyzeVoiceInput(text, 'frontend-test-user');
      setAnalysis({ 
        priority: res.priority, 
        confidence: res.confidence, 
        reasoning: res.reasoning 
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to analyze input');
    } finally {
      setIsAnalyzing(false);
    }
  }, [text]);

  const handleCreate = useCallback(async () => {
    if (!text.trim()) return;
    setError(null);
    setIsCreating(true);
    setCreated(null);

    try {
      let result;
      let method: string;

      if (inputMode === 'voice') {
        // Use voice API for voice input
        const voiceResult = await apiService.createVoiceEvent(text, 'frontend-test-user');
        result = {
          success: voiceResult.success,
          id: voiceResult.event_id,
          title: (voiceResult.event_data?.title as string) || text
        };
        method = 'voice';
      } else {
        // Use voice API for consistent NLP parsing but mark as text input
        const voiceResult = await apiService.createVoiceEvent(text, 'frontend-test-user');
        
        // Update the event to mark it as text input for proper icon display
        if (voiceResult.success && voiceResult.event_id) {
          try {
            await apiService.updateEvent(voiceResult.event_id, { created_via: 'text' }, 'frontend-test-user');
          } catch (e) {
            console.warn('Failed to update created_via field:', e);
          }
        }
        
        result = {
          success: voiceResult.success,
          id: voiceResult.event_id,
          title: (voiceResult.event_data?.title as string) || text
        };
        method = 'text';
      }

      if (result.success && result.id) {
        setCreated({ 
          id: result.id, 
          title: result.title,
          method 
        });
        setText('');
        setAnalysis(null);
        onEventCreated?.();
        // Auto-dismiss after 3 seconds
        setTimeout(() => setCreated(null), 3000);
      } else {
        setError('Failed to create event');
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to create event');
    } finally {
      setIsCreating(false);
    }
  }, [text, inputMode, analysis, onEventCreated]);

  const handleTextFocus = useCallback(() => {
    if (!isListening) {
      setInputMode('text');
    }
  }, [isListening]);

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        {inputMode === 'voice' ? '🎤' : '✏️'} Quick Event Creator
        <span className="ml-2 text-sm font-normal text-gray-500">
          ({inputMode === 'voice' ? 'Voice Mode' : 'Text Mode'})
        </span>
      </h2>

      <div className="flex items-center space-x-2">
        {/* Main Input Field */}
        <div className="flex-1 relative">
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            onFocus={handleTextFocus}
            placeholder={
              isListening 
                ? "Listening... speak now" 
                : inputMode === 'voice' 
                  ? "Click microphone to speak or type here..."
                  : "e.g., Meeting with Alex tomorrow at 3pm for 45m"
            }
            onKeyDown={(e) => {
              if (e.key === 'Enter' && canSubmit) {
                e.preventDefault();
                handleCreate();
              }
              if (e.key === 'Escape') setText('');
            }}
            className={`w-full px-3 py-2 text-sm border rounded-lg focus:ring-2 focus:border-transparent ${
              isListening 
                ? 'border-purple-300 bg-purple-50 focus:ring-purple-500' 
                : 'border-gray-300 focus:ring-purple-500'
            }`}
            disabled={isListening}
          />
          {isListening && (
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse animation-delay-100"></div>
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse animation-delay-200"></div>
              </div>
            </div>
          )}
        </div>

        {/* Voice Button */}
        <button
          type="button"
          onClick={isListening ? handleVoiceStop : handleVoiceStart}
          disabled={!recognition || isCreating || isAnalyzing}
          className={`p-2 rounded-lg transition-colors ${
            isListening
              ? 'bg-red-600 text-white hover:bg-red-700'
              : 'bg-purple-600 text-white hover:bg-purple-700 disabled:bg-gray-300'
          }`}
          title={isListening ? "Stop listening" : "Start voice input"}
        >
          {isListening ? (
            <StopIcon className="h-5 w-5" />
          ) : (
            <MicrophoneIcon className="h-5 w-5" />
          )}
        </button>

        {/* Preview Button */}
        <button
          type="button"
          onClick={handleAnalyze}
          disabled={!text.trim() || isAnalyzing || isListening}
          className="px-3 py-2 text-sm rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 flex items-center"
          title="Preview BERT analysis"
        >
          <SparklesIcon className="h-4 w-4 mr-1" /> 
          {isAnalyzing ? 'Analyzing...' : 'Preview'}
        </button>

        {/* Create Button */}
        <button
          type="button"
          onClick={handleCreate}
          disabled={!canSubmit}
          className="px-4 py-2 text-sm rounded-lg bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50 flex items-center"
        >
          <PencilIcon className="h-4 w-4 mr-1" />
          {isCreating ? 'Creating...' : 'Create'}
        </button>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <div className="text-sm text-blue-800">
            <div className="font-medium">
              {(() => {
                const { label: priorityLabel } = getPriorityLabel(analysis.priority);
                return `Priority: ${priorityLabel} • Confidence: ${Math.round(analysis.confidence * 100)}%`;
              })()}
            </div>
            {analysis.reasoning && (
              <div className="text-xs text-blue-600 mt-1">💡 {analysis.reasoning}</div>
            )}
          </div>
        </div>
      )}

      {/* Success Message */}
      {created && (
        <div className="mt-3 p-3 bg-green-50 rounded-lg border border-green-200 flex items-center">
          <CheckCircleIcon className="h-4 w-4 mr-2 text-green-600" />
          <div className="text-sm text-green-800">
            <span className="font-medium">Event Created!</span>
            <div className="text-xs">
              "{created.title}" via {created.method === 'voice' ? '🎤 Voice' : '✏️ Text'}
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-3 p-3 bg-red-50 rounded-lg border border-red-200">
          <div className="text-sm text-red-800">{error}</div>
        </div>
      )}

      {/* Mode Indicator */}
      <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
        <div>
          Input mode: {inputMode === 'voice' ? '🎤 Voice' : '✏️ Text'} • 
          Press Enter to create • ESC to clear
        </div>
        {recognition && (
          <div>Voice recognition: Available</div>
        )}
      </div>
    </div>
  );
};

export default UnifiedEventCreator;
