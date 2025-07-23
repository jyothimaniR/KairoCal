import React from 'react';

const ConflictAlert = ({ onDismiss }) => {
  const handleReviewClick = () => {
    // TODO: Navigate to event detail or show conflict resolution modal
    alert('This would show the conflict resolution interface.\n\nConflict: "Yoga Class" overlaps with "Team Meeting" on June 13th at 4:30 PM.');
  };

  return (
    <div style={{
      backgroundColor: '#fef3c7',
      border: '1px solid #f59e0b',
      borderRadius: '12px',
      padding: '16px 20px',
      display: 'flex',
      alignItems: 'flex-start',
      gap: '12px',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
    }}>
      {/* Alert Icon */}
      <div style={{
        fontSize: '20px',
        marginTop: '2px',
        flexShrink: 0
      }}>
        🔔
      </div>

      {/* Content */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          gap: '12px'
        }}>
          <div>
            <h4 style={{
              fontSize: '16px',
              fontWeight: '600',
              color: '#92400e',
              margin: '0 0 4px 0'
            }}>
              Conflict Detected
            </h4>
            <p style={{
              fontSize: '14px',
              color: '#78350f',
              margin: '0 0 8px 0',
              lineHeight: '1.4'
            }}>
              "Yoga Class" has been moved to 4:30 PM due to a schedule conflict with "Team Meeting".
            </p>
            <button
              onClick={handleReviewClick}
              style={{
                background: 'none',
                border: 'none',
                color: '#92400e',
                fontSize: '14px',
                fontWeight: '600',
                textDecoration: 'underline',
                cursor: 'pointer',
                padding: 0,
                margin: 0
              }}
              onMouseEnter={(e) => e.target.style.color = '#78350f'}
              onMouseLeave={(e) => e.target.style.color = '#92400e'}
            >
              Review →
            </button>
          </div>

          {/* Dismiss Button */}
          <button
            onClick={onDismiss}
            style={{
              background: 'none',
              border: 'none',
              color: '#92400e',
              fontSize: '18px',
              cursor: 'pointer',
              padding: '4px',
              borderRadius: '4px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background-color 0.2s',
              flexShrink: 0
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(146, 64, 14, 0.1)'}
            onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
            title="Dismiss notification"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConflictAlert;