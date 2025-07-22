import React, { useRef } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction';

// Mock events for testing
const today = new Date().toISOString().slice(0, 10);
const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().slice(0, 10);

const mockEvents = [
  { 
    id: '1',
    title: 'Team Meeting', 
    date: today,
    color: '#3788d8'
  },
  { 
    id: '2',
    title: 'Doctor Appointment', 
    date: tomorrow,
    color: '#ff6b6b'
  },
  { 
    id: '3',
    title: 'Project Deadline', 
    date: '2025-07-25',
    color: '#4ecdc4'
  },
  {
    id: '4',
    title: 'Conference Call',
    start: `${today}T10:00:00`,
    end: `${today}T11:00:00`,
    color: '#45b7d1'
  }
];

const Calendar = ({
  initialView = 'dayGridMonth',
  onDateClick = () => {},
  onEventClick = () => {},
  calendarRef,
  events = mockEvents
}) => {
  const localRef = useRef();
  const calRef = calendarRef || localRef;

  const handleDateClick = (info) => {
    console.log('📅 Date clicked:', info.dateStr);
    onDateClick(info);
  };

  const handleEventClick = (info) => {
    console.log('🎯 Event clicked:', info.event.title);
    onEventClick(info);
  };

  return (
    <div style={{ 
      background: '#ffffff', 
      borderRadius: '12px', 
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', 
      padding: '24px',
      minHeight: '600px',
      border: '1px solid #e5e7eb'
    }}>
      <div style={{ marginBottom: '16px' }}>
        <h2 style={{ 
          margin: 0, 
          color: '#1f2937', 
          fontSize: '1.5rem',
          fontWeight: '600'
        }}>
          📅 Your Smart Calendar
        </h2>
        <p style={{ 
          margin: '4px 0 0 0', 
          color: '#6b7280',
          fontSize: '0.9rem'
        }}>
          AI-powered event management
        </p>
      </div>
      
      <FullCalendar
        ref={calRef}
        plugins={[dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin]}
        initialView={initialView}
        initialDate={new Date()}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        }}
        events={events}
        dateClick={handleDateClick}
        eventClick={handleEventClick}
        height="600px"
        selectable={true}
        selectMirror={true}
        dayMaxEvents={3}
        weekends={true}
        nowIndicator={true}
        editable={true}
        droppable={true}
        views={{
          dayGridMonth: { 
            buttonText: 'Month',
            dayMaxEventRows: 3
          },
          timeGridWeek: { 
            buttonText: 'Week',
            slotMinTime: '06:00:00',
            slotMaxTime: '22:00:00'
          },
          timeGridDay: { 
            buttonText: 'Day',
            slotMinTime: '06:00:00',
            slotMaxTime: '22:00:00'
          },
          listWeek: { 
            buttonText: 'List' 
          }
        }}
        eventColor="#3788d8"
        eventTextColor="#ffffff"
        eventBorderColor="transparent"
        eventClassNames="fc-event-custom"
      />
    </div>
  );
};

export default Calendar;