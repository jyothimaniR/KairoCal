import React, { useCallback, useState } from 'react';
import { SparklesIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';
import { voiceService } from '../../services/voiceService';

interface QuickSchedulerProps {
  onEventCreated?: () => void;
}

const QuickScheduler: React.FC<QuickSchedulerProps> = ({ onEventCreated }) => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<{
    priority: number;
    confidence: number;
    reasoning: string;
  } | null>(null);
  const [created, setCreated] = useState<{ id: string; title: string } | null>(null);

  const canSubmit = text.trim().length > 0 && !isAnalyzing && !isCreating;

  const handleAnalyze = useCallback(async () => {
    if (!text.trim()) return;
    setError(null);
    setAnalysis(null);
    setIsAnalyzing(true);
    try {
      const res = await voiceService.analyzeVoiceInput(text, 'frontend-test-user');
      setAnalysis({ priority: res.priority, confidence: res.confidence, reasoning: res.reasoning });
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
      // Use regular event creation API for text input (not voice API)
      const eventData = {
        title: text,
        description: `Created via text input: ${text}`,
        start_time: new Date().toISOString(),
        end_time: new Date(Date.now() + 60 * 60 * 1000).toISOString(), // 1 hour default
        created_via: 'manual', // This is TEXT input, not voice
        priority_level: 3 // Default priority
      };
      
      const result = await apiService.createEvent(eventData, 'frontend-test-user');
      
      if (result && result.id) {
        const title = result.title || text;
        setCreated({ id: result.id, title });
        setText('');
        setAnalysis(null);
        onEventCreated?.();
        // Auto-dismiss the created banner after 3 seconds
        setTimeout(() => setCreated(null), 3000);
      } else {
        setError('Failed to create event');
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to create event');
    } finally {
      setIsCreating(false);
    }
  }, [text, onEventCreated]);

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        ✍️ Quick Add (Type to schedule)
      </h2>

      <div className="flex items-center space-x-2">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="e.g., Meeting with Alex tomorrow at 3pm for 45m"
          onKeyDown={(e) => {
            if (e.key === 'Enter' && canSubmit) {
              e.preventDefault();
              handleCreate();
            }
            if (e.key === 'Escape') setText('');
          }}
          className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        />
        <button
          type="button"
          onClick={handleAnalyze}
          disabled={!text.trim() || isAnalyzing}
          className="px-3 py-2 text-sm rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50"
          title="Preview interpretation"
        >
          <SparklesIcon className="h-4 w-4 inline mr-1" /> Preview
        </button>
        <button
          type="button"
          onClick={handleCreate}
          disabled={!canSubmit}
          className="px-3 py-2 text-sm rounded-lg bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50"
        >
          Create
        </button>
      </div>

      {analysis && (
        <div className="mt-3 text-sm text-gray-700">
          <div>
            Priority: {analysis.priority} • Confidence: {Math.round(analysis.confidence * 100)}%
          </div>
          {analysis.reasoning && (
            <div className="text-xs text-gray-500 mt-1">💡 {analysis.reasoning}</div>
          )}
        </div>
      )}

      {created && (
        <div className="mt-3 text-sm text-green-700 flex items-center">
          <CheckCircleIcon className="h-4 w-4 mr-1" /> Created: "{created.title}" (ID: {created.id})
        </div>
      )}

      {error && (
        <div className="mt-3 text-sm text-red-700">{error}</div>
      )}
    </div>
  );
};

export default QuickScheduler;
