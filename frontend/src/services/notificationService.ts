// Chat-app style notification service for KairoCal
// Only shows badge when there are NEW unread notifications

export interface Notification {
  id: string;
  type: 'conflict' | 'upcoming' | 'priority';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  actionable?: boolean;
  eventId?: string;
  severity: 'high' | 'medium' | 'low';
}

export class NotificationService {
  private static notifications: Notification[] = [];
  private static listeners: Array<(notifications: Notification[]) => void> = [];

  static addNotification(notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) {
    const newNotification: Notification = {
      ...notification,
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date(),
      read: false // Always starts as unread
    };
    
    this.notifications.unshift(newNotification);
    // Keep only last 20 notifications
    if (this.notifications.length > 20) {
      this.notifications = this.notifications.slice(0, 20);
    }
    
    this.notifyListeners();
  }

  static getNotifications(): Notification[] {
    return [...this.notifications];
  }

  static getUnreadCount(): number {
    return this.notifications.filter(n => !n.read).length;
  }

  static markAsRead(id: string) {
    const notification = this.notifications.find(n => n.id === id);
    if (notification) {
      notification.read = true;
      this.notifyListeners();
    }
  }

  static markAllAsRead() {
    this.notifications.forEach(n => n.read = true);
    this.notifyListeners();
  }

  // Remove a specific notification
  static dismissNotification(id: string) {
    this.notifications = this.notifications.filter(n => n.id !== id);
    this.notifyListeners();
  }

  static subscribe(listener: (notifications: Notification[]) => void) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  private static notifyListeners() {
    this.listeners.forEach(listener => listener([...this.notifications]));
  }

  // Smart notification generation with anti-spam (no rate limiting)
  static generateSmartNotifications(events: any[], conflicts: any[]) {
    // Get existing notification IDs to avoid duplicates
    const existingConflictIds = new Set(
      this.notifications
        .filter(n => n.type === 'conflict')
        .map(n => n.eventId)
    );
    
    const existingUpcomingIds = new Set(
      this.notifications
        .filter(n => n.type === 'upcoming')
        .map(n => n.eventId)
    );

    const now = new Date();

    // 1. 🚨 CONFLICTS - Always notify for new conflicts only
    conflicts.forEach(conflict => {
      const conflictId = `${conflict.event1?.id}-${conflict.event2?.id}`;
      if (!existingConflictIds.has(conflictId)) {
        this.addNotification({
          type: 'conflict',
          severity: 'high',
          title: 'Schedule Conflict',
          message: `"${conflict.event1?.title}" overlaps with "${conflict.event2?.title}"`,
          actionable: true,
          eventId: conflictId
        });
      }
    });

    // 2. ⏰ UPCOMING EVENTS - Only for next 15 minutes, avoid duplicates
    const fifteenMinutesFromNow = new Date(now.getTime() + 15 * 60 * 1000);
    
    events.forEach(event => {
      if (!event.start_time || existingUpcomingIds.has(event.id)) return;
      const eventStart = new Date(event.start_time);
      
      if (eventStart > now && eventStart <= fifteenMinutesFromNow) {
        const minutesUntil = Math.round((eventStart.getTime() - now.getTime()) / (1000 * 60));
        this.addNotification({
          type: 'upcoming',
          severity: 'medium',
          title: 'Event Starting Soon',
          message: `"${event.title}" starts in ${minutesUntil} minutes`,
          actionable: true,
          eventId: event.id
        });
      }
    });

    // 3. 🎯 HIGH PRIORITY - Only Critical (Priority 5) events for today, max 3
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const criticalEventsToday = events.filter(event => {
      if (!event.start_time || event.priority_level !== 5) return false;
      const eventDate = new Date(event.start_time);
      return eventDate >= today && eventDate < tomorrow;
    });

    // Only notify if there are 3 or fewer critical events (avoid spam)
    if (criticalEventsToday.length <= 3) {
      const existingPriorityIds = new Set(
        this.notifications
          .filter(n => n.type === 'priority')
          .map(n => n.eventId)
      );

      criticalEventsToday.forEach(event => {
        if (!existingPriorityIds.has(event.id)) {
          this.addNotification({
            type: 'priority',
            severity: 'medium',
            title: 'Critical Event Today',
            message: `"${event.title}" requires immediate attention`,
            actionable: true,
            eventId: event.id
          });
        }
      });
    }
  }

  // Clean up old notifications (older than 24 hours)
  static cleanupOldNotifications() {
    const twentyFourHoursAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    this.notifications = this.notifications.filter(n => n.timestamp > twentyFourHoursAgo);
    this.notifyListeners();
  }

  // Add a test notification for demo purposes
  static addTestNotification() {
    this.addNotification({
      type: 'conflict',
      severity: 'high',
      title: 'Test Notification',
      message: 'This is a test notification to demonstrate the system',
      actionable: false
    });
  }

  // Development helper - add sample notifications for testing
  static addSampleNotifications() {
    this.addNotification({
      type: 'conflict',
      severity: 'high',
      title: 'Schedule Conflict Detected',
      message: 'Meeting with John overlaps with Team Standup at 2:00 PM',
      actionable: true
    });

    this.addNotification({
      type: 'upcoming',
      severity: 'medium',
      title: 'Upcoming Event',
      message: 'Project Review meeting starts in 15 minutes',
      actionable: true
    });

    this.addNotification({
      type: 'priority',
      severity: 'high',
      title: 'High Priority Event',
      message: 'Board Meeting (Priority 9) scheduled for today',
      actionable: true
    });
  }

  // Development helper - clear all notifications
  static clearAllNotifications() {
    this.notifications = [];
    this.notifyListeners();
  }
}
