/**
 * Centralized Priority System for KairoCal
 * Ensures consistent priority mapping across all components
 * STANDARDIZED TO BERT SCALE: 1 (VERY LOW) to 5 (CRITICAL)
 */

export interface PriorityInfo {
  level: number;
  label: string;
  color: string;
  bgColor: string;
  textColor: string;
}

/**
 * BERT Standard Priority Scale: 1 (VERY LOW) to 5 (CRITICAL)
 * This matches the BERT model output exactly - no conversion needed
 * BERT assigns priority 5 to critical events like "URGENT emergency meeting with CEO"
 */
export const PRIORITY_MAPPING: Record<number, PriorityInfo> = {
  1: {
    level: 1,
    label: 'VERY LOW',
    color: 'green',
    bgColor: 'bg-green-100',
    textColor: 'text-green-800'
  },
  2: {
    level: 2, 
    label: 'LOW',
    color: 'blue',
    bgColor: 'bg-blue-100',
    textColor: 'text-blue-800'
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
    label: 'HIGH',
    color: 'orange', 
    bgColor: 'bg-orange-100',
    textColor: 'text-orange-800'
  },
  5: {
    level: 5,
    label: 'CRITICAL',
    color: 'red',
    bgColor: 'bg-red-100', 
    textColor: 'text-red-800'
  }
};

/**
 * Get priority information for a given priority level (BERT standard)
 * @param priority Priority level (1-5, where 5 is CRITICAL)
 * @param fallback Fallback priority if input is invalid
 * @returns PriorityInfo object with BERT scale mapping
 */
export const getPriorityInfo = (priority: number | undefined | null, fallback: number = 3): PriorityInfo => {
  // Normalize priority to valid range
  const normalizedPriority = normalizePriority(priority || fallback);
  
  // Use BERT scale directly - no conversion needed
  return PRIORITY_MAPPING[normalizedPriority];
};

/**
 * Get priority label only (BERT standard)
 * @param priority Priority level (1-5, where 5 is CRITICAL)
 * @returns Object with label and color
 */
export const getPriorityLabel = (priority: number): { label: string; color: string } => {
  const normalizedPriority = normalizePriority(priority);
  const info = getPriorityInfo(normalizedPriority);
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
 * Format priority for display with confidence (BERT standard)
 * @param priority Priority level (1-5, where 5 is CRITICAL)
 * @param confidence Confidence score (0-1)
 * @returns Formatted string
 */
export const formatPriorityWithConfidence = (priority: number, confidence: number): string => {
  const info = getPriorityInfo(priority);
  const confidencePercent = Math.round(confidence * 100);
  return `${info.label} (${confidencePercent}% confidence)`;
};

/**
 * Get CSS classes for priority styling (BERT standard)
 * @param priority Priority level (1-5, where 5 is CRITICAL)
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
