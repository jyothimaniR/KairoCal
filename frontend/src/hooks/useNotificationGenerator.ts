import { useEffect } from 'react';
import { useDashboard } from './useDashboard';
import { NotificationService } from '../services/notificationService';

export const useNotificationGenerator = () => {
  const { events } = useDashboard();

  useEffect(() => {
    if (!events.length) return;

    // Generate notifications based on current data
    NotificationService.generateSmartNotifications(events, []);

    // Set up periodic checking for upcoming events (every 5 minutes)
    const interval = setInterval(() => {
      NotificationService.generateSmartNotifications(events, []);
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, [events]);

  // Additional helper to manually trigger notification generation
  const refreshNotifications = () => {
    NotificationService.generateSmartNotifications(events, []);
  };

  return { refreshNotifications };
};
