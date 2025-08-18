/**
 * Priority Components Index
 * 
 * NEW MODULE: Exports all priority-related components for easy importing
 * These components supplement existing functionality without breaking anything.
 */

export { default as PriorityEditor } from './PriorityEditor';
export { default as PriorityTimeSlotSelector } from './PriorityTimeSlotSelector';

// Type exports for convenience
export type { default as PriorityEditorProps } from './PriorityEditor';
export type { default as PriorityTimeSlotSelectorProps } from './PriorityTimeSlotSelector';

// Priority level constants for reuse
export const PRIORITY_LEVELS = [
  { level: 1, name: 'Very Low', color: 'text-gray-500', icon: '🔽' },
  { level: 2, name: 'Low', color: 'text-blue-500', icon: '⚡' },
  { level: 3, name: 'Medium', color: 'text-yellow-500', icon: '🔸' },
  { level: 4, name: 'High', color: 'text-orange-500', icon: '🔥' },
  { level: 5, name: 'Critical', color: 'text-red-500', icon: '🚨' }
];

// Helper function to get priority configuration
export const getPriorityConfig = (level: number) => {
  return PRIORITY_LEVELS.find(p => p.level === level) || PRIORITY_LEVELS[2];
};
