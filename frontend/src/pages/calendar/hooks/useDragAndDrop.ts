import { useState, useRef } from 'react';
import type { Event } from '../../../services/apiService';

export interface DragState {
  isDragging: boolean;
  draggedEvent: Event | null;
  dragOffset: { x: number; y: number };
  originalPosition: { x: number; y: number };
  currentPosition: { x: number; y: number };
  previewTime: Date | null;
  conflictingEvents: Event[];
}

export interface DropZone {
  date: Date;
  timeSlot: number; // minutes from start of day
  isValid: boolean;
  conflictingEvents: Event[];
}

export const useDragAndDrop = (
  events: Event[],
  onEventMove: (eventId: string, newStartTime: Date, newEndTime: Date) => Promise<boolean>
) => {
  const [dragState, setDragState] = useState<DragState>({
    isDragging: false,
    draggedEvent: null,
    dragOffset: { x: 0, y: 0 },
    originalPosition: { x: 0, y: 0 },
    currentPosition: { x: 0, y: 0 },
    previewTime: null,
    conflictingEvents: [],
  });

  const dragTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const PIXELS_PER_MINUTE = 1.333; // 80px per hour = 1.333px per minute

  // Check for conflicting events at a given time
  const checkConflicts = (
    targetStartTime: Date,
    targetEndTime: Date,
    excludeEventId: string
  ): Event[] => {
    return events.filter(event => {
      if (event.id === excludeEventId) return false;
      
      const eventStart = new Date(event.start_time);
      const eventEnd = new Date(event.end_time);
      
      return (
        (targetStartTime >= eventStart && targetStartTime < eventEnd) ||
        (targetEndTime > eventStart && targetEndTime <= eventEnd) ||
        (targetStartTime <= eventStart && targetEndTime >= eventEnd)
      );
    });
  };

  // Convert mouse position to time slot
  const positionToTime = (
    y: number,
    containerRef: HTMLElement,
    baseDate: Date
  ): Date => {
    const rect = containerRef.getBoundingClientRect();
    const relativeY = y - rect.top;
    const minutes = Math.max(0, Math.round(relativeY / PIXELS_PER_MINUTE));
    
    // TIMEZONE FIX: Create new date using local time components to avoid timezone conversion
    // Use explicit local time construction to prevent automatic UTC conversion
    const targetTime = new Date(baseDate.getFullYear(), baseDate.getMonth(), baseDate.getDate());
    targetTime.setMinutes(minutes);
    
    // CRITICAL: Ensure we're working in local time, not UTC
    // This prevents the 1-hour offset issue when dragging events
    return targetTime;
  };

  // Start dragging an event
  const handleDragStart = (
    event: Event,
    mouseEvent: React.MouseEvent,
    containerRef: HTMLElement
  ) => {
    if (dragTimeoutRef.current) {
      clearTimeout(dragTimeoutRef.current);
    }

    const rect = containerRef.getBoundingClientRect();
    const offsetX = mouseEvent.clientX - rect.left;
    const offsetY = mouseEvent.clientY - rect.top;

    setDragState({
      isDragging: true,
      draggedEvent: event,
      dragOffset: { x: offsetX, y: offsetY },
      originalPosition: { x: mouseEvent.clientX, y: mouseEvent.clientY },
      currentPosition: { x: mouseEvent.clientX, y: mouseEvent.clientY },
      previewTime: new Date(event.start_time),
      conflictingEvents: [],
    });

    // Prevent text selection during drag
    document.body.style.userSelect = 'none';
    document.body.style.cursor = 'grabbing';
  };

  // Update drag position and check for conflicts
  const handleDragMove = (
    mouseEvent: MouseEvent,
    containerRef: HTMLElement,
    baseDate: Date
  ) => {
    if (!dragState.isDragging || !dragState.draggedEvent) return;

    const newTime = positionToTime(mouseEvent.clientY, containerRef, baseDate);
    const eventDuration = new Date(dragState.draggedEvent.end_time).getTime() - 
                         new Date(dragState.draggedEvent.start_time).getTime();
    const newEndTime = new Date(newTime.getTime() + eventDuration);

    const conflicts = checkConflicts(newTime, newEndTime, dragState.draggedEvent.id || '');

    setDragState(prev => ({
      ...prev,
      currentPosition: { x: mouseEvent.clientX, y: mouseEvent.clientY },
      previewTime: newTime,
      conflictingEvents: conflicts,
    }));
  };

  // Complete the drag operation
  const handleDragEnd = async (
    _containerRef: HTMLElement,
    _baseDate: Date
  ): Promise<boolean> => {
    if (!dragState.isDragging || !dragState.draggedEvent || !dragState.previewTime) {
      resetDragState();
      return false;
    }

    const eventDuration = new Date(dragState.draggedEvent.end_time).getTime() - 
                         new Date(dragState.draggedEvent.start_time).getTime();
    const newEndTime = new Date(dragState.previewTime.getTime() + eventDuration);

    // Check if there are conflicts
    if (dragState.conflictingEvents.length > 0) {
      // Show conflict warning but allow the move
      const confirmMove = window.confirm(
        `This event will conflict with ${dragState.conflictingEvents.length} other event(s). Continue?`
      );
      
      if (!confirmMove) {
        resetDragState();
        return false;
      }
    }

    try {
      const success = await onEventMove(
        dragState.draggedEvent.id || '',
        dragState.previewTime,
        newEndTime
      );

      if (success) {
        console.log('✅ Event successfully moved via drag & drop');
      } else {
        console.error('❌ Failed to move event');
      }

      resetDragState();
      return success;
    } catch (error) {
      console.error('❌ Error during drag & drop:', error);
      resetDragState();
      return false;
    }
  };

  // Cancel drag operation
  const handleDragCancel = () => {
    resetDragState();
  };

  // Reset drag state
  const resetDragState = () => {
    setDragState({
      isDragging: false,
      draggedEvent: null,
      dragOffset: { x: 0, y: 0 },
      originalPosition: { x: 0, y: 0 },
      currentPosition: { x: 0, y: 0 },
      previewTime: null,
      conflictingEvents: [],
    });

    document.body.style.userSelect = '';
    document.body.style.cursor = '';

    if (dragTimeoutRef.current) {
      clearTimeout(dragTimeoutRef.current);
    }
  };

  // Get drop zone validation
  const getDropZoneInfo = (
    mouseY: number,
    containerRef: HTMLElement,
    baseDate: Date,
    draggedEvent: Event
  ): DropZone | null => {
    if (!draggedEvent) return null;

    const targetTime = positionToTime(mouseY, containerRef, baseDate);
    const eventDuration = new Date(draggedEvent.end_time).getTime() - 
                         new Date(draggedEvent.start_time).getTime();
    const targetEndTime = new Date(targetTime.getTime() + eventDuration);

    const conflicts = checkConflicts(targetTime, targetEndTime, draggedEvent.id || '');

    return {
      date: baseDate,
      timeSlot: targetTime.getHours() * 60 + targetTime.getMinutes(),
      isValid: true, // Allow moves even with conflicts (with warning)
      conflictingEvents: conflicts,
    };
  };

  return {
    dragState,
    handleDragStart,
    handleDragMove,
    handleDragEnd,
    handleDragCancel,
    getDropZoneInfo,
    resetDragState,
  };
};
