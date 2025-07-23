const today = new Date().toISOString().slice(0, 10);
const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
const dayAfterTomorrow = new Date(Date.now() + 48 * 60 * 60 * 1000).toISOString().slice(0, 10);

export const mockEvents = [
  { 
    id: '1',
    title: 'Team Meeting', 
    start: `${today}T10:00:00`,
    end: `${today}T11:00:00`,
    color: '#3788d8'
  },
  { 
    id: '2',
    title: 'Interview', 
    start: `${today}T14:00:00`,
    end: `${today}T15:00:00`,
    color: '#ff6b6b'
  },
  { 
    id: '3',
    title: 'Doctor Appointment', 
    start: `${tomorrow}T09:00:00`,
    end: `${tomorrow}T10:00:00`,
    color: '#4ecdc4'
  },
  {
    id: '4',
    title: 'Project Review',
    start: `${tomorrow}T15:30:00`,
    end: `${tomorrow}T16:30:00`,
    color: '#45b7d1'
  },
  {
    id: '5',
    title: 'Marathon Run 10k',
    start: `${dayAfterTomorrow}T08:00:00`,
    end: `${dayAfterTomorrow}T10:00:00`,
    color: '#96ceb4'
  },
  {
    id: '6',
    title: 'Lunch with Colleagues',
    start: `${dayAfterTomorrow}T12:00:00`,
    end: `${dayAfterTomorrow}T13:00:00`,
    color: '#feca57'
  }
];