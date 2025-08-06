import { useState, useCallback, useRef } from 'react';
import { voiceService } from '../services/voiceService';
import type { VoiceAnalysisResponse, VoiceEventResponse } from '../services/voiceService';

export interface VoiceState {
  isListening: boolean;
  isProcessing: boolean;
  transcript: string;
  error: string | null;
  lastResult: VoiceAnalysisResponse | null;
  isSupported: boolean;
}

export const useVoice = () => {
  const [state, setState] = useState<VoiceState>({
    isListening: false,
    isProcessing: false,
    transcript: '',
    error: null,
    lastResult: null,
    isSupported: ('webkitSpeechRecognition' in window) || ('SpeechRecognition' in window)
  });

  const recognitionRef = useRef<any>(null);

  const startListening = useCallback(async () => {
    if (!state.isSupported) {
      setState(prev => ({ ...prev, error: 'Speech recognition not supported in this browser' }));
      return;
    }

    try {
      setState(prev => ({ 
        ...prev, 
        isListening: true, 
        error: null, 
        transcript: '',
        lastResult: null 
      }));

      const transcript = await voiceService.startVoiceRecognition();
      
      setState(prev => ({ 
        ...prev, 
        transcript, 
        isListening: false, 
        isProcessing: true 
      }));

      // Analyze the voice input
      const analysis = await voiceService.analyzeVoiceInput(transcript);
      
      setState(prev => ({ 
        ...prev, 
        lastResult: analysis, 
        isProcessing: false 
      }));

      return { transcript, analysis };
    } catch (error) {
      console.error('Voice recognition error:', error);
      setState(prev => ({ 
        ...prev, 
        isListening: false, 
        isProcessing: false, 
        error: error instanceof Error ? error.message : 'Voice recognition failed' 
      }));
      throw error;
    }
  }, [state.isSupported]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setState(prev => ({ 
      ...prev, 
      isListening: false, 
      isProcessing: false 
    }));
  }, []);

  const createEvent = useCallback(async (voiceText: string): Promise<VoiceEventResponse> => {
    try {
      setState(prev => ({ ...prev, isProcessing: true, error: null }));
      
      const result = await voiceService.createEventFromVoice(voiceText);
      
      setState(prev => ({ ...prev, isProcessing: false }));
      
      return result;
    } catch (error) {
      console.error('Voice event creation error:', error);
      setState(prev => ({ 
        ...prev, 
        isProcessing: false, 
        error: error instanceof Error ? error.message : 'Failed to create event' 
      }));
      throw error;
    }
  }, []);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const reset = useCallback(() => {
    setState(prev => ({ 
      ...prev, 
      transcript: '', 
      error: null, 
      lastResult: null,
      isListening: false,
      isProcessing: false
    }));
  }, []);

  return {
    ...state,
    startListening,
    stopListening,
    createEvent,
    clearError,
    reset
  };
};

export default useVoice;
