/**
 * Centralized Priority System for KairoCal
 * Ensures consistent priority mapping across all components
 */

export interface PriorityInfo {
  level: number;
  label: string;
  color: string;
  bgColor: string;
  textColor: string;
}

/**
 * Standard priority scale: 1 (CRITICAL) to 5 (VERY LOW) 
 * NOTE: BERT model returns high numbers for high priority (CEO=5), but UI expects 1=highest
 * So we invert: BERT 5 -> UI 1, BERT 4 -> UI 2, etc.
 */
export const PRIORITY_MAPPING: Record<number, PriorityInfo> = {
  1: {
    level: 1,
    label: 'CRITICAL',
    color: 'red',
    bgColor: 'bg-red-100',
    textColor: 'text-red-800'
  },
  2: {
    level: 2, 
    label: 'HIGH',
    color: 'orange',
    bgColor: 'bg-orange-100',
    textColor: 'text-orange-800'
  },
  3: {
    level: 3,
    label: 'MEDIUM', 
    color: 'yellow',
    bgColor: 'bg-yellow-100',
    textColor: 'text-yellow-800'
  },
  4: {
    level: 4,
    label: 'LOW',
    color: 'blue', 
    bgColor: 'bg-blue-100',
    textColor: 'text-blue-800'
  },
  5: {
    level: 5,
    label: 'VERY LOW',
    color: 'green',
    bgColor: 'bg-green-100', 
    textColor: 'text-green-800'
  }
};

/**
 * Convert BERT priority (1-5, high number = high priority) to UI priority (1-5, low number = high priority)
 */
export const convertBertPriorityToUI = (bertPriority: number): number => {
  // Invert the scale: BERT 5 -> UI 1, BERT 4 -> UI 2, BERT 3 -> UI 3, BERT 2 -> UI 4, BERT 1 -> UI 5
  return Math.max(1, Math.min(5, 6 - Math.floor(bertPriority || 3)));
};

/**
 * Get priority information for a given BERT priority level
 * @param bertPriority BERT Priority level (1-5, higher = more important)
 * @param fallback Fallback priority if input is invalid
 * @returns PriorityInfo object
 */
export const getPriorityInfo = (bertPriority: number | undefined | null, fallback: number = 3): PriorityInfo => {
  const uiPriority = convertBertPriorityToUI(bertPriority || fallback);
  return PRIORITY_MAPPING[uiPriority];
};

/**
 * Get priority label only (legacy compatibility)
 * @param bertPriority BERT Priority level (1-5, higher = more important)
 * @returns Object with label and color
 */
export const getPriorityLabel = (bertPriority: number): { label: string; color: string } => {
  const info = getPriorityInfo(bertPriority);
  return { label: info.label, color: info.color };
};

/**
 * Validate and normalize priority value
 * @param priority Input priority
 * @returns Valid priority between 1-5
 */
export const normalizePriority = (priority: number | string | undefined | null): number => {
  if (typeof priority === 'string') {
    priority = parseInt(priority, 10);
  }
  if (!priority || isNaN(priority)) {
    return 3; // Default medium priority
  }
  return Math.max(1, Math.min(5, Math.floor(priority)));
};

/**
 * Format priority for display with confidence
 * @param priority Priority level
 * @param confidence Confidence score (0-1)
 * @returns Formatted string
 */
export const formatPriorityWithConfidence = (priority: number, confidence: number): string => {
  const info = getPriorityInfo(priority);
  const confidencePercent = Math.round(confidence * 100);
  return `${info.label} (${confidencePercent}% confidence)`;
};

/**
 * Get CSS classes for priority styling
 * @param priority Priority level
 * @returns Object with CSS classes
 */
export const getPriorityClasses = (priority: number) => {
  const info = getPriorityInfo(priority);
  return {
    badge: `${info.bgColor} ${info.textColor} px-2 py-1 rounded`,
    border: `border-l-4 border-${info.color}-400`,
    text: info.textColor,
    bg: info.bgColor
  };
};

export default {
  PRIORITY_MAPPING,
  getPriorityInfo,
  getPriorityLabel,
  normalizePriority,
  formatPriorityWithConfidence,
  getPriorityClasses
};
