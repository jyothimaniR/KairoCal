import React, { useRef } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction';

const today = new Date().toISOString().slice(0, 10);
const mockEvents = [
  { title: 'Test Event', date: '2025-07-22' },
  { title: 'Meeting', date: '2025-07-23' },
  { title: 'Conference', date: '2025-07-24' },
  { title: 'Today Event', date: today }
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

  return (
    <div style={{ background: '#f5f6fa', borderRadius: 8, boxShadow: '0 2px 8px #eee', padding: 16, minHeight: 600 }}>
      <FullCalendar
        ref={calRef}
        plugins={[dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin]}
        initialView={initialView}
        initialDate={new Date()}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay,listYear'
        }}
        events={events}
        dateClick={onDateClick}
        eventClick={onEventClick}
        height="600px"
        selectable={true}
        dayMaxEvents={3}
        views={{
          dayGridMonth: { buttonText: 'Month' },
          timeGridWeek: { buttonText: 'Week' },
          timeGridDay: { buttonText: 'Day' },
          listYear: { buttonText: 'Year' }
        }}
      />
    </div>
  );
};

export default Calendar;
