import React, { useMemo, useState } from 'react';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import type { Event } from '../../services/apiService';

export interface MiniCalendarProps {
  events: Event[];
  selectedDate?: Date;
  onSelectDate?: (date: Date) => void;
}

const dayKey = (d: Date) => {
  const y = d.getFullYear();
  const m = `${d.getMonth() + 1}`.padStart(2, '0');
  const day = `${d.getDate()}`.padStart(2, '0');
  return `${y}-${m}-${day}`;
};

const startOfMonth = (d: Date) => new Date(d.getFullYear(), d.getMonth(), 1);
const endOfMonth = (d: Date) => new Date(d.getFullYear(), d.getMonth() + 1, 0);
const isSameDay = (a: Date, b: Date) =>
  a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

const MiniCalendar: React.FC<MiniCalendarProps> = ({ events, selectedDate, onSelectDate }) => {
  const today = useMemo(() => new Date(), []);
  const [cursor, setCursor] = useState<Date>(selectedDate || today);
  const selected = selectedDate || today;

  const monthStart = startOfMonth(cursor);
  const monthEnd = endOfMonth(cursor);
  const startWeekday = monthStart.getDay(); // 0 Sun - 6 Sat
  const daysInMonth = monthEnd.getDate();

  const eventsByDay = useMemo(() => {
    const map = new Map<string, number>();
    for (const e of events || []) {
      if (!e.start_time) continue;
      const d = new Date(e.start_time);
      const key = dayKey(d);
      map.set(key, (map.get(key) || 0) + 1);
    }
    return map;
  }, [events]);

  const gridDays: Array<{ date: Date; inMonth: boolean } > = useMemo(() => {
    const days: Array<{ date: Date; inMonth: boolean }> = [];
    // Leading blanks from previous month
    for (let i = 0; i < startWeekday; i++) {
      const d = new Date(monthStart);
      d.setDate(d.getDate() - (startWeekday - i));
      days.push({ date: d, inMonth: false });
    }
    // Current month
    for (let i = 1; i <= daysInMonth; i++) {
      days.push({ date: new Date(cursor.getFullYear(), cursor.getMonth(), i), inMonth: true });
    }
    // Trailing to complete 6 rows (42 cells)
    while (days.length % 7 !== 0 || days.length < 42) {
      const last = days[days.length - 1].date;
      const d = new Date(last);
      d.setDate(d.getDate() + 1);
      days.push({ date: d, inMonth: false });
    }
    return days;
  }, [cursor, monthStart, startWeekday, daysInMonth]);

  const monthName = cursor.toLocaleString(undefined, { month: 'long' });
  const year = cursor.getFullYear();

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center justify-between">
        <span>{monthName} {year}</span>
        <div className="flex space-x-1">
          <button
            className="p-1 hover:bg-gray-100 rounded"
            aria-label="Previous month"
            onClick={() => setCursor(new Date(cursor.getFullYear(), cursor.getMonth() - 1, 1))}
          >
            <ChevronLeftIcon className="h-4 w-4" />
          </button>
          <button
            className="p-1 hover:bg-gray-100 rounded"
            aria-label="Next month"
            onClick={() => setCursor(new Date(cursor.getFullYear(), cursor.getMonth() + 1, 1))}
          >
            <ChevronRightIcon className="h-4 w-4" />
          </button>
        </div>
      </h3>

      <div className="grid grid-cols-7 gap-1 text-center text-xs">
        {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((d, index) => (
          <div key={`dow-${index}`} className="p-2 text-gray-500 font-medium">{d}</div>
        ))}

        {gridDays.map(({ date, inMonth }) => {
          const key = dayKey(date);
          const count = eventsByDay.get(key) || 0;
          const isToday = isSameDay(date, today);
          const isSelected = isSameDay(date, selected);
          const base = inMonth ? 'text-gray-900' : 'text-gray-400';
          const sel = isSelected ? 'bg-purple-600 text-white' : isToday ? 'bg-purple-100 text-purple-700' : 'hover:bg-gray-100';
          const ring = isSelected ? 'ring-2 ring-purple-400' : '';

          return (
            <button
              key={key}
              className={`relative p-2 text-sm rounded ${base} ${sel} ${ring}`}
              onClick={() => onSelectDate?.(date)}
            >
              <span>{date.getDate()}</span>
              {count > 0 && (
                <span className="absolute bottom-1 right-1 text-[10px] px-1 py-0.5 rounded bg-purple-50 text-purple-700 border border-purple-200">
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default MiniCalendar;
