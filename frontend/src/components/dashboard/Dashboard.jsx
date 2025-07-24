import React, { useState } from 'react';
import { Grid, Box, Typography, Paper } from '@mui/material';

// Your existing calendar component
import Calendar from '../calendar/Calendar';

// Mock data - you can move this to separate files later
const mockEvents = [
  { 
    id: '1',
    title: 'Team Meeting', 
    start: '2025-07-23T10:00:00',
    end: '2025-07-23T11:00:00',
    color: '#3788d8'
  },
  { 
    id: '2',
    title: 'Interview', 
    start: '2025-07-23T14:00:00',
    end: '2025-07-23T15:00:00',
    color: '#ff6b6b'
  },
  { 
    id: '3',
    title: 'Doctor Appointment', 
    start: '2025-07-24T09:00:00',
    end: '2025-07-24T10:00:00',
    color: '#4ecdc4'
  },
  {
    id: '4',
    title: 'Project Review',
    start: '2025-07-24T15:30:00',
    end: '2025-07-24T16:30:00',
    color: '#45b7d1'
  },
  {
    id: '5',
    title: 'Marathon Run 10k',
    start: '2025-07-25T08:00:00',
    end: '2025-07-25T10:00:00',
    color: '#96ceb4'
  }
];

const searchPrompts = [
  "What's on your mind?",
  "Try: Meeting at 4pm tomorrow at campus",
  "Schedule: Doctor appointment next Friday",
  "Add: Team lunch this Thursday at noon",
  "Create: Conference call at 9am Monday",
  "Book: Gym session tomorrow evening"
];

// Search Input Component
const SearchInput = ({ onSearch, onVoiceInput }) => {
  const [inputValue, setInputValue] = useState('');
  const [currentPromptIndex, setCurrentPromptIndex] = useState(0);
  const [isListening, setIsListening] = useState(false);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPromptIndex(prev => (prev + 1) % searchPrompts.length);
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
    setIsListening(!isListening);
    onVoiceInput(isListening ? 'stop' : 'start');
  };

  return (
    <Box sx={{ mb: 3, maxWidth: 600 }}>
      <form onSubmit={handleSubmit}>
        <div style={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center'
        }}>
          <div style={{
            position: 'absolute',
            left: '16px',
            zIndex: 1,
            color: '#9ca3af',
            fontSize: '18px'
          }}>
            🔍
          </div>

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
              transition: 'all 0.2s ease'
            }}
          >
            {isListening ? '⏹️' : '🎤'}
          </button>
        </div>

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
    </Box>
  );
};

// REMOVED: ConflictAlert Component - No longer needed

// Upcoming Events Component
const UpcomingEvents = ({ events = [] }) => {
  const [showNext3Days, setShowNext3Days] = useState(true);

  // Get today's date
  const today = new Date();
  const todayStr = today.toISOString().split('T')[0];
  
  // Get next 3 days dates
  const next3Days = [];
  for (let i = 1; i <= 3; i++) {
    const nextDay = new Date(today);
    nextDay.setDate(today.getDate() + i);
    next3Days.push(nextDay.toISOString().split('T')[0]);
  }

  // Filter events for today
  const todayEvents = events
    .filter(event => {
      const eventDate = event.start ? event.start.split('T')[0] : event.date;
      return eventDate === todayStr;
    })
    .slice(0, 3);

  // Filter events for next 3 days
  const upcomingEvents = events
    .filter(event => {
      const eventDate = event.start ? event.start.split('T')[0] : event.date;
      return next3Days.includes(eventDate);
    })
    .sort((a, b) => {
      const dateA = a.start || a.date;
      const dateB = b.start || b.date;
      return new Date(dateA) - new Date(dateB);
    });

  const formatTime = (eventTime) => {
    if (!eventTime) return '';
    
    const time = eventTime.includes('T') ? 
      eventTime.split('T')[1].substring(0, 5) : '';
    
    if (!time) return '';
    
    const [hours, minutes] = time.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    
    return `${displayHour}:${minutes}${ampm}`;
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    
    if (dateStr === today.toISOString().split('T')[0]) {
      return 'Today';
    } else if (dateStr === tomorrow.toISOString().split('T')[0]) {
      return 'Tomorrow';
    } else {
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      });
    }
  };

  return (
    <Paper sx={{
      borderRadius: '12px',
      border: '1px solid #e5e7eb',
      padding: '24px',
      height: 'fit-content'
    }}>
      <Typography variant="h6" sx={{
        fontSize: '18px',
        fontWeight: 600,
        color: '#1f2937',
        margin: '0 0 20px 0',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        📅 Upcoming Events
      </Typography>

      {/* Today's Events */}
      <div style={{ marginBottom: '24px' }}>
        <Typography variant="subtitle2" sx={{
          fontSize: '14px',
          fontWeight: 600,
          color: '#374151',
          margin: '0 0 12px 0',
          textTransform: 'uppercase',
          letterSpacing: '0.5px'
        }}>
          Today
        </Typography>

        {todayEvents.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {todayEvents.map((event, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  padding: '12px',
                  backgroundColor: '#f0f9ff',
                  borderRadius: '8px',
                  border: '1px solid #e0f2fe'
                }}
              >
                <div
                  style={{
                    width: '12px',
                    height: '12px',
                    borderRadius: '50%',
                    backgroundColor: event.color || '#3788d8',
                    marginRight: '12px',
                    flexShrink: 0
                  }}
                />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{
                    fontSize: '14px',
                    fontWeight: '500',
                    color: '#1f2937',
                    marginBottom: '2px',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap'
                  }}>
                    {event.title}
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: '#0369a1',
                    fontWeight: '600'
                  }}>
                    {formatTime(event.start) || '10:00AM'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{
            padding: '16px',
            textAlign: 'center',
            color: '#9ca3af',
            fontSize: '14px',
            backgroundColor: '#f9fafb',
            borderRadius: '8px',
            border: '1px dashed #d1d5db'
          }}>
            No events today
          </div>
        )}
      </div>

      {/* Next 3 Days */}
      <div>
        <div 
          onClick={() => setShowNext3Days(!showNext3Days)}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            marginBottom: '12px',
            padding: '4px 0'
          }}
        >
          <Typography variant="subtitle2" sx={{
            fontSize: '14px',
            fontWeight: 600,
            color: '#374151',
            margin: 0,
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Next 3 Days ({upcomingEvents.length})
          </Typography>
          <div style={{
            fontSize: '12px',
            color: '#6b7280',
            transform: showNext3Days ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s'
          }}>
            ▼
          </div>
        </div>

        {showNext3Days && (
          <div>
            {upcomingEvents.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {upcomingEvents.map((event, index) => {
                  const eventDate = event.start ? event.start.split('T')[0] : event.date;
                  return (
                    <div
                      key={index}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '12px',
                        backgroundColor: '#fefefe',
                        borderRadius: '8px',
                        border: '1px solid #f3f4f6',
                        transition: 'all 0.2s'
                      }}
                    >
                      <div
                        style={{
                          width: '12px',
                          height: '12px',
                          borderRadius: '50%',
                          backgroundColor: event.color || '#3788d8',
                          marginRight: '12px',
                          flexShrink: 0
                        }}
                      />
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{
                          fontSize: '14px',
                          fontWeight: '500',
                          color: '#1f2937',
                          marginBottom: '2px',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }}>
                          {event.title}
                        </div>
                        <div style={{
                          fontSize: '12px',
                          color: '#6b7280',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px'
                        }}>
                          <span>{formatDate(eventDate)}</span>
                          {formatTime(event.start) && (
                            <>
                              <span>•</span>
                              <span style={{ color: '#4f46e5', fontWeight: '600' }}>
                                {formatTime(event.start)}
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div style={{
                padding: '16px',
                textAlign: 'center',
                color: '#9ca3af',
                fontSize: '14px',
                backgroundColor: '#f9fafb',
                borderRadius: '8px',
                border: '1px dashed #d1d5db'
              }}>
                No upcoming events
              </div>
            )}
          </div>
        )}
      </div>
    </Paper>
  );
};

// Main Dashboard Component
const Dashboard = () => {
  const [events, setEvents] = useState(mockEvents);
  // REMOVED: const [hasConflict, setHasConflict] = useState(true);
  // REMOVED: const [conflictDismissed, setConflictDismissed] = useState(false);

  const handleSearch = (query) => {
    console.log('🔍 Search query:', query);
    alert(`Processing: "${query}"\n\nThis will create a calendar event using AI/NLP processing.`);
  };

  const handleVoiceInput = (action) => {
    console.log('🎤 Voice input:', action);
    if (action === 'start') {
      console.log('Starting voice recognition...');
    } else if (action === 'stop') {
      console.log('Stopping voice recognition...');
    }
  };

  const handleDateClick = (info) => {
    const confirmed = window.confirm(
      `Create a new event on ${info.dateStr}?\n\nThis would open the event creation modal in the full app.`
    );
    
    if (confirmed) {
      console.log('Creating event for:', info.dateStr);
    }
  };

  const handleEventClick = (info) => {
    const confirmed = window.confirm(
      `Event: ${info.event.title}\n\nWould you like to edit this event?`
    );
    
    if (confirmed) {
      console.log('Editing event:', info.event.title);
    }
  };

  // REMOVED: const handleConflictDismiss = () => { setConflictDismissed(true); };

  return (
    <Box sx={{ 
      maxWidth: '1400px',
      margin: '0 auto',
      padding: '24px'
    }}>
      {/* Search/Input Section */}
      <SearchInput 
        onSearch={handleSearch}
        onVoiceInput={handleVoiceInput}
      />

      {/* REMOVED: Conflict Alert */}
      {/* {hasConflict && !conflictDismissed && (
        <ConflictAlert onDismiss={handleConflictDismiss} />
      )} */}

      {/* Main Content Grid */}
      <Grid container spacing={3}>
        {/* Calendar Section */}
        <Grid item xs={12} lg={8}>
          <Calendar 
            events={events}
            onDateClick={handleDateClick}
            onEventClick={handleEventClick}
          />
        </Grid>

        {/* Events Sidebar */}
        <Grid item xs={12} lg={4}>
          <UpcomingEvents events={events} />
        </Grid>
      </Grid>

      {/* Bottom Status */}
      <Paper sx={{
        marginTop: '32px',
        padding: '20px',
        borderRadius: '12px',
        border: '1px solid #e5e7eb',
        textAlign: 'center'
      }}>
        <div style={{
          fontSize: '24px',
          marginBottom: '8px'
        }}>
          👍
        </div>
        <Typography variant="h6" sx={{
          fontSize: '16px',
          fontWeight: 600,
          color: '#1f2937',
          marginBottom: '4px'
        }}>
          You're all set for the day!
        </Typography>
        <Typography variant="body2" sx={{
          fontSize: '14px',
          color: '#6b7280'
        }}>
          Your calendar is up to date and conflicts are resolved.
        </Typography>
      </Paper>

      {/* CSS for animations */}
      <style>
        {`
          @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.05); }
            100% { opacity: 1; transform: scale(1); }
          }
        `}
      </style>
    </Box>
  );
};

export default Dashboard;