import { useState, useEffect } from 'react';
import { NotificationService, type Notification } from '../services/notificationService';

export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    // Initial load
    setNotifications(NotificationService.getNotifications());
    setUnreadCount(NotificationService.getUnreadCount());

    // Subscribe to updates
    const unsubscribe = NotificationService.subscribe((newNotifications) => {
      setNotifications(newNotifications);
      setUnreadCount(NotificationService.getUnreadCount());
    });

    // Cleanup old notifications daily
    const cleanup = setInterval(() => {
      NotificationService.cleanupOldNotifications();
    }, 60 * 60 * 1000); // Every hour

    return () => {
      unsubscribe();
      clearInterval(cleanup);
    };
  }, []);

  const markAsRead = (id: string) => {
    NotificationService.markAsRead(id);
  };

  const markAllAsRead = () => {
    NotificationService.markAllAsRead();
  };

  const dismissNotification = (id: string) => {
    NotificationService.dismissNotification(id);
  };

  return {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
    dismissNotification
  };
};
