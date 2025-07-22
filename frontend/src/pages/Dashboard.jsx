import React from 'react';
import { logout } from '../services/authService';
import Calendar from '../components/calendar/Calendar';

const Dashboard = () => {
  const handleLogout = () => {
    console.log('🚪 Dashboard: Logging out...');
    logout();
  };

  const handleDateClick = (info) => {
    alert(`Date clicked: ${info.dateStr}\n\nIn the full app, this would open the event creation modal.`);
  };

  const handleEventClick = (info) => {
    alert(`Event clicked: ${info.event.title}\n\nIn the full app, this would open the event details modal.`);
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#f8fafc',
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    }}>
      {/* Header */}
      <header style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 1.5rem'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            height: '64px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <h1 style={{
                fontSize: '1.5rem',
                fontWeight: 'bold',
                margin: 0,
                color: 'white'
              }}>
                📅 KairoCal
              </h1>
              <span style={{
                fontSize: '0.875rem',
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                padding: '4px 8px',
                borderRadius: '12px',
                fontWeight: '500'
              }}>
                AI Calendar
              </span>
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <span style={{
                fontSize: '0.875rem',
                opacity: 0.9
              }}>
                Welcome back! 👋
              </span>
              <button
                onClick={handleLogout}
                style={{
                  padding: '8px 16px',
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseOver={(e) => {
                  e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
                }}
                onMouseOut={(e) => {
                  e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
                }}
              >
                🚪 Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '2rem 1.5rem'
      }}>
        {/* Welcome Section */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '1.5rem',
          marginBottom: '2rem',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
          border: '1px solid #e5e7eb'
        }}>
          <h2 style={{
            fontSize: '1.25rem',
            fontWeight: '600',
            color: '#1f2937',
            margin: '0 0 0.5rem 0'
          }}>
            🎉 Welcome to your AI-Powered Calendar
          </h2>
          <p style={{
            color: '#6b7280',
            margin: '0 0 1rem 0',
            lineHeight: '1.5'
          }}>
            You are successfully authenticated via AWS Cognito. Your calendar is ready for intelligent event management.
          </p>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1rem',
            marginTop: '1rem'
          }}>
            <div style={{
              padding: '1rem',
              backgroundColor: '#f0f9ff',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>🤖</div>
              <div style={{ fontSize: '0.875rem', fontWeight: '500', color: '#0369a1' }}>
                AI Event Creation
              </div>
            </div>
            <div style={{
              padding: '1rem',
              backgroundColor: '#f0fdf4',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>⚡</div>
              <div style={{ fontSize: '0.875rem', fontWeight: '500', color: '#166534' }}>
                Smart Scheduling
              </div>
            </div>
            <div style={{
              padding: '1rem',
              backgroundColor: '#fef3f2',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>🔔</div>
              <div style={{ fontSize: '0.875rem', fontWeight: '500', color: '#dc2626' }}>
                Intelligent Notifications
              </div>
            </div>
            <div style={{
              padding: '1rem',
              backgroundColor: '#f5f3ff',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>☁️</div>
              <div style={{ fontSize: '0.875rem', fontWeight: '500', color: '#7c3aed' }}>
                Cloud-Native
              </div>
            </div>
          </div>
        </div>

        {/* Calendar Section */}
        <div style={{ marginBottom: '2rem' }}>
          <Calendar 
            onDateClick={handleDateClick}
            onEventClick={handleEventClick}
          />
        </div>

        {/* Development Status */}
        <div style={{
          background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
          borderRadius: '12px',
          padding: '1.5rem',
          textAlign: 'center',
          border: '1px solid #fed7aa'
        }}>
          <h3 style={{
            fontSize: '1.125rem',
            fontWeight: '600',
            color: '#9a3412',
            margin: '0 0 0.5rem 0'
          }}>
            🚧 Development Status
          </h3>
          <p style={{
            color: '#9a3412',
            margin: '0',
            fontSize: '0.875rem'
          }}>
            This is your KairoCal MVP dashboard. The calendar is fully functional with FullCalendar v6.
            Click on dates or events to see interaction capabilities!
          </p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;