import React, { useState, useEffect } from 'react';
import { searchPrompts } from '../../config/searchPrompts';

const SearchInput = ({ onSearch, onVoiceInput }) => {
  const [currentPromptIndex, setCurrentPromptIndex] = useState(0);
  const [inputValue, setInputValue] = useState('');
  const [isListening, setIsListening] = useState(false);

  // Cycle through prompts every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPromptIndex((prev) => 
        (prev + 1) % searchPrompts.length
      );
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSearch(inputValue.trim());
      setInputValue('');
    }
  };

  const handleVoiceClick = () => {
    if (isListening) {
      // Stop listening
      setIsListening(false);
      onVoiceInput('stop');
    } else {
      // Start listening
      setIsListening(true);
      onVoiceInput('start');
      
      // Auto-stop after 30 seconds
      setTimeout(() => {
        setIsListening(false);
        onVoiceInput('stop');
      }, 30000);
    }
  };

  return (
    <div style={{
      marginBottom: '24px',
      maxWidth: '600px'
    }}>
      <form onSubmit={handleSubmit}>
        <div style={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center'
        }}>
          {/* Search Icon */}
          <div style={{
            position: 'absolute',
            left: '16px',
            zIndex: 1,
            color: '#9ca3af',
            fontSize: '18px'
          }}>
            🔍
          </div>

          {/* Input Field */}
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={searchPrompts[currentPromptIndex]}
            style={{
              width: '100%',
              padding: '14px 60px 14px 48px',
              fontSize: '16px',
              border: '2px solid #e5e7eb',
              borderRadius: '12px',
              backgroundColor: 'white',
              color: '#1f2937',
              outline: 'none',
              transition: 'all 0.2s ease',
              fontFamily: "'Inter', sans-serif"
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#4f46e5';
              e.target.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.1)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = '#e5e7eb';
              e.target.style.boxShadow = 'none';
            }}
          />

          {/* Voice/Mic Button */}
          <button
            type="button"
            onClick={handleVoiceClick}
            style={{
              position: 'absolute',
              right: '12px',
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: isListening ? '#ef4444' : '#f3f4f6',
              color: isListening ? 'white' : '#6b7280',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '16px',
              transition: 'all 0.2s ease',
              animation: isListening ? 'pulse 1.5s infinite' : 'none'
            }}
            onMouseEnter={(e) => {
              if (!isListening) {
                e.target.style.backgroundColor = '#e5e7eb';
                e.target.style.color = '#374151';
              }
            }}
            onMouseLeave={(e) => {
              if (!isListening) {
                e.target.style.backgroundColor = '#f3f4f6';
                e.target.style.color = '#6b7280';
              }
            }}
            title={isListening ? 'Click to stop listening' : 'Click to start voice input'}
          >
            {isListening ? '⏹️' : '🎤'}
          </button>
        </div>

        {/* Voice Status */}
        {isListening && (
          <div style={{
            marginTop: '8px',
            fontSize: '12px',
            color: '#ef4444',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <div style={{
              width: '6px',
              height: '6px',
              borderRadius: '50%',
              backgroundColor: '#ef4444',
              animation: 'pulse 1s infinite'
            }} />
            Listening... Speak now or click stop
          </div>
        )}

        {/* Helper Text */}
        <div style={{
          marginTop: '8px',
          fontSize: '12px',
          color: '#9ca3af',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <span>
            Try: "Meeting tomorrow at 2pm" or "Dentist appointment next Friday"
          </span>
          <span>
            Press Enter to create event
          </span>
        </div>
      </form>

      <style>
        {`
          @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.05); }
            100% { opacity: 1; transform: scale(1); }
          }
        `}
      </style>
    </div>
  );
};

export default SearchInput;