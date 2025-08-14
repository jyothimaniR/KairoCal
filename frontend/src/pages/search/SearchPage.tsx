import React, { useMemo, useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { MagnifyingGlassIcon, MicrophoneIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useDashboard } from '../../hooks/useDashboard';
import { useVoice } from '../../hooks/useVoice';

const SearchPage: React.FC = () => {
  const { events } = useDashboard();
  const [query, setQuery] = useState('');
  const location = useLocation() as { state?: { q?: string } };
  useEffect(() => {
    if (location.state?.q) setQuery(location.state.q);
  }, [location.state]);
  const {
    isListening,
    isProcessing,
    transcript,
    startListening,
    stopListening,
    reset,
  } = useVoice();

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return events.filter(e => `${e.title} ${e.description ?? ''}`.toLowerCase().includes(q));
  }, [events, query]);

  const onMicClick = async () => {
    if (isListening) {
      stopListening();
      return;
    }
    try {
      const res = await startListening();
      if (res?.transcript) {
        setQuery(res.transcript);
      }
    } catch {
      // ignore
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Search</h1>
      <div className="relative max-w-xl">
        <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder={transcript ? transcript : 'Search events...'}
          className="w-full pl-10 pr-20 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        />
        {query && (
          <button
            type="button"
            aria-label="Clear search"
            title="Clear search"
            onClick={() => { setQuery(''); reset(); }}
            className="absolute right-10 top-1/2 -translate-y-1/2"
          >
            <XMarkIcon className="h-5 w-5 text-gray-400" />
          </button>
        )}
        <button
          type="button"
          aria-label={isListening ? 'Stop voice input' : 'Start voice input'}
          title={isListening ? 'Stop voice input' : 'Start voice input'}
          onClick={onMicClick}
          className="absolute right-3 top-1/2 -translate-y-1/2"
        >
          <MicrophoneIcon className={`h-5 w-5 ${isListening ? 'text-red-500' : 'text-purple-500'}`} />
        </button>
      </div>

      <div className="mt-6">
        {isProcessing && <div className="text-sm text-gray-500">Analyzing voice...</div>}
        {!query && <div className="text-sm text-gray-500">Type to search your events.</div>}
        {query && results.length === 0 && (
          <div className="text-sm text-gray-500">No results for "{query}"</div>
        )}
        {results.length > 0 && (
          <ul className="divide-y divide-gray-200 border border-gray-200 rounded-lg">
            {results.map(ev => (
              <li key={ev.id} className="p-3">
                <div className="text-sm font-medium text-gray-900">{ev.title}</div>
                {ev.description && <div className="text-xs text-gray-600 mt-1">{ev.description}</div>}
                <div className="text-xs text-gray-500 mt-1">{new Date(ev.start_time).toLocaleString()}</div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
