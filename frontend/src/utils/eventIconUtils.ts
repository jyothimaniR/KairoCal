/**
 * Event Emoji/Icon Mapping System
 * Maps event types to appropriate emojis for consistent display
 */

export interface EventIconInfo {
  emoji: string;
  category: string;
  color: string;
}

// Event category mapping based on keywords and context
export const EVENT_CATEGORIES = {
  // Work & Business
  meeting: { emoji: '👥', category: 'work', color: 'blue' },
  standup: { emoji: '🗣️', category: 'work', color: 'blue' },
  presentation: { emoji: '📊', category: 'work', color: 'purple' },
  review: { emoji: '🔍', category: 'work', color: 'orange' },
  planning: { emoji: '📋', category: 'work', color: 'green' },
  project: { emoji: '🏗️', category: 'work', color: 'yellow' },
  call: { emoji: '📞', category: 'work', color: 'blue' },
  client: { emoji: '🤝', category: 'work', color: 'green' },
  interview: { emoji: '💼', category: 'work', color: 'purple' },
  
  // Food & Social  
  lunch: { emoji: '🍽️', category: 'social', color: 'orange' },
  dinner: { emoji: '🍽️', category: 'social', color: 'red' },
  brunch: { emoji: '🥐', category: 'social', color: 'yellow' },
  breakfast: { emoji: '🌅', category: 'social', color: 'yellow' },
  coffee: { emoji: '☕', category: 'social', color: 'brown' },
  drinks: { emoji: '🍻', category: 'social', color: 'amber' },
  
  // Health & Personal
  doctor: { emoji: '🏥', category: 'health', color: 'red' },
  dentist: { emoji: '🦷', category: 'health', color: 'blue' },
  appointment: { emoji: '📅', category: 'personal', color: 'gray' },
  workout: { emoji: '💪', category: 'health', color: 'green' },
  gym: { emoji: '🏋️', category: 'health', color: 'red' },
  
  // Learning & Development
  training: { emoji: '🎓', category: 'education', color: 'blue' },
  workshop: { emoji: '🔧', category: 'education', color: 'orange' },
  course: { emoji: '📚', category: 'education', color: 'green' },
  lecture: { emoji: '🎤', category: 'education', color: 'purple' },
  
  // Entertainment
  movie: { emoji: '🎬', category: 'entertainment', color: 'purple' },
  concert: { emoji: '🎵', category: 'entertainment', color: 'pink' },
  party: { emoji: '🎉', category: 'entertainment', color: 'rainbow' },
  game: { emoji: '🎮', category: 'entertainment', color: 'blue' },
  
  // Travel & Transportation
  flight: { emoji: '✈️', category: 'travel', color: 'blue' },
  trip: { emoji: '🧳', category: 'travel', color: 'brown' },
  commute: { emoji: '🚗', category: 'travel', color: 'gray' },
  
  // Default fallbacks based on priority
  critical: { emoji: '🚨', category: 'urgent', color: 'red' },
  urgent: { emoji: '⚡', category: 'urgent', color: 'yellow' },
  important: { emoji: '⭐', category: 'important', color: 'orange' },
  
  // Generic fallbacks
  event: { emoji: '📅', category: 'general', color: 'blue' },
  task: { emoji: '✅', category: 'general', color: 'green' },
  reminder: { emoji: '🔔', category: 'general', color: 'yellow' },
  default: { emoji: '📋', category: 'general', color: 'gray' }
};

/**
 * Get emoji for an event based on title and context
 */
export const getEventIcon = (
  title: string = '',
  _category?: string,
  priority: number = 3,
  createdVia: string = 'manual'
): string => {
  const text = `${title}`.toLowerCase();
  
  // Check for keywords in title
  for (const [keyword, iconInfo] of Object.entries(EVENT_CATEGORIES)) {
    if (text.includes(keyword)) {
      return iconInfo.emoji;
    }
  }
  
  // Priority-based fallback
  if (priority === 1) return EVENT_CATEGORIES.critical.emoji;
  if (priority === 2) return EVENT_CATEGORIES.important.emoji;
  
  // Created via fallback
  if (createdVia === 'voice') return '🎤';
  if (createdVia === 'imported') return '📥';
  
  // Default event icon
  return '📅';
};

/**
 * Get full event icon info for an event
 */
export const getEventIconInfo = (
  title: string = '',
  _category?: string,
  priority: number = 3,
  createdVia: string = 'manual'
): EventIconInfo => {
  const text = `${title}`.toLowerCase();
  
  // Check for keywords in title
  for (const [keyword, iconInfo] of Object.entries(EVENT_CATEGORIES)) {
    if (text.includes(keyword)) {
      return iconInfo;
    }
  }
  
  // Priority-based fallback
  if (priority === 1) return EVENT_CATEGORIES.critical;
  if (priority === 2) return EVENT_CATEGORIES.important;
  
  // Created via fallback
  if (createdVia === 'voice') return { emoji: '🎤', category: 'voice', color: 'purple' };
  if (createdVia === 'imported') return { emoji: '📥', category: 'imported', color: 'blue' };
  
  // Default
  return EVENT_CATEGORIES.default;
};

/**
 * Get formatted display string with emoji
 */
export const formatEventTitle = (
  title: string,
  priority?: number,
  createdVia?: string
): string => {
  const emoji = getEventIcon(title, undefined, priority, createdVia);
  return `${emoji} ${title}`;
};

export default {
  EVENT_CATEGORIES,
  getEventIcon,
  getEventIconInfo,
  formatEventTitle
};
