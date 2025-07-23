import React, { useState } from 'react';

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
    .slice(0, 3); // Max 3 events

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
    
    // Convert 24h to 12h format
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
    <div style={{
      backgroundColor: 'white',
      borderRadius: '12px',
      border: '1px solid #e5e7eb',
      padding: '24px',
      height: 'fit-content'
    }}>
      {/* Header */}
      <h3 style={{
        fontSize: '18px',
        fontWeight: '600',
        color: '#1f2937',
        margin: '0 0 20px 0',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        📅 Upcoming Events
      </h3>

      {/* Today's Events */}
      <div style={{ marginBottom: '24px' }}>
        <h4 style={{
          fontSize: '14px',
          fontWeight: '600',
          color: '#374151',
          margin: '0 0 12px 0',
          textTransform: 'uppercase',
          letterSpacing: '0.5px'
        }}>
          Today
        </h4>

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
          <h4 style={{
            fontSize: '14px',
            fontWeight: '600',
            color: '#374151',
            margin: 0,
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Next 3 Days ({upcomingEvents.length})
          </h4>
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
                      onMouseEnter={(e) => {
                        e.target.style.backgroundColor = '#f9fafb';
                        e.target.style.borderColor = '#e5e7eb';
                      }}
                      onMouseLeave={(e) => {
                        e.target.style.backgroundColor = '#fefefe';
                        e.target.style.borderColor = '#f3f4f6';
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
    </div>
  );
};

export default UpcomingEvents;