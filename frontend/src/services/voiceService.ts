/**
 * Voice Service - Connects frontend to KairoCal Voice API with BERT classification
 */

import { API_V1 } from '../config/api';

export interface VoiceTranscribeResponse {
  transcribed_text: string;
  cleaned_text: string;
  confidence: number;
  processing_time: number;
  timestamp: string;
  metadata: {
  [key: string]: unknown;
  };
}

export interface VoiceEventResponse {
  success: boolean;
  event_id?: string;
  event_data: {
  [key: string]: unknown;
  };
  nlp_analysis: {
  [key: string]: unknown;
  };
  bert_classification: {
    priority: number;
    confidence: number;
    reasoning: string;
  };
  processing_details: {
  [key: string]: unknown;
  };
  message: string;
}

export interface VoiceAnalysisResponse {
  priority: number;
  confidence: number;
  reasoning: string;
  keywords: string[];
  sentiment: string;
  urgency_score: number;
}

class VoiceService {
  
  /**
   * Test voice API health
   */
  async testVoiceHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_V1}/voice/health`);
      const data = await response.json();
      return data.status === 'healthy';
    } catch (error) {
      console.error('Voice health check failed:', error);
      return false;
    }
  }

  /**
   * Transcribe and clean voice text
   */
  async transcribeVoice(text: string, userId?: string): Promise<VoiceTranscribeResponse> {
    try {
      const response = await fetch(`${API_V1}/voice/transcribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          user_id: userId,
          language: 'en',
          confidence_threshold: 0.5
        }),
      });

      if (!response.ok) {
        throw new Error(`Voice transcription failed: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Voice transcription error:', error);
      throw error;
    }
  }

  /**
   * Create event from voice input using BERT classification
   */
  async createEventFromVoice(voiceText: string, userId: string = 'frontend-test-user'): Promise<VoiceEventResponse> {
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

    console.log('⏱️ Voice service using duration preference:', durationPreference);

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
          priority_override: null,
          duration_preference: durationPreference
        }),
      });

      if (!response.ok) {
        throw new Error(`Voice event creation failed: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Voice event creation error:', error);
      throw error;
    }
  }

  /**
   * Analyze voice input for priority using BERT
   */
  async analyzeVoiceInput(voiceText: string, userId: string = 'frontend-test-user'): Promise<VoiceAnalysisResponse> {
    try {
      console.log('🔍 Analyzing voice input:', voiceText);
      console.log('🌐 API URL:', `${API_V1}/voice/analyze-voice`);
      
      const response = await fetch(`${API_V1}/voice/analyze-voice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          voice_text: voiceText,
          user_id: userId,
          include_bert: true,
          detailed_analysis: true
        }),
      });

      console.log('📡 Response status:', response.status);
      console.log('📡 Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ API Error Response:', errorText);
        throw new Error(`Voice analysis failed: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Analysis result:', data);
      
      return {
        priority: data.bert_classification?.priority || data.priority || 3,
        confidence: data.bert_classification?.confidence || data.confidence || 0.5,
        reasoning: data.bert_classification?.reasoning || data.reasoning || 'Analysis complete',
        keywords: data.nlp_analysis?.keywords || [],
        sentiment: data.nlp_analysis?.sentiment || 'neutral',
        urgency_score: data.nlp_analysis?.urgency_score || 0.5
      };
    } catch (error) {
      console.error('Voice analysis error:', error);
      throw error;
    }
  }

  /**
   * Web Speech API Integration - Browser native voice recognition
   */
  startVoiceRecognition(): Promise<string> {
    return new Promise((resolve, reject) => {
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        reject(new Error('Speech recognition not supported in this browser'));
        return;
      }

      const SpeechRecognitionCtor =
        (window as unknown as { SpeechRecognition?: unknown }).SpeechRecognition ||
        (window as unknown as { webkitSpeechRecognition?: unknown }).webkitSpeechRecognition;
      const Ctor = SpeechRecognitionCtor as new () => {
        continuous: boolean;
        interimResults: boolean;
        maxAlternatives: number;
        lang: string;
        onstart: () => void;
        onresult: (event: Event) => void;
        onerror: (event: Event) => void;
        onend: () => void;
        start: () => void;
      };
      const recognition = new Ctor();

      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        console.log('🎤 Voice recognition started');
      };

      recognition.onresult = (event: Event) => {
        const e = event as unknown as { results: Array<Array<{ transcript: string; confidence: number }>> };
        const transcript = e.results[0][0].transcript;
        const confidence = e.results[0][0].confidence;
        
        console.log(`🗣️ Recognized: "${transcript}" (confidence: ${confidence})`);
        resolve(transcript);
      };

      recognition.onerror = (event: Event) => {
        const err: string = (event as unknown as { error?: string }).error || 'unknown_error';
        console.error('Voice recognition error:', err);
        reject(new Error(`Voice recognition failed: ${err}`));
      };

      recognition.onend = () => {
        console.log('🎤 Voice recognition ended');
      };

      recognition.start();
    });
  }
}

export const voiceService = new VoiceService();
export default voiceService;
