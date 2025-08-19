import { NotificationService } from '../services/notificationService';

// Development helper object for browser console testing
const NotificationDev = {
  // Add sample notifications for testing
  addSamples: () => {
    NotificationService.addSampleNotifications();
    console.log('✅ Added sample notifications');
  },

  // Clear all notifications
  clear: () => {
    NotificationService.clearAllNotifications();
    console.log('🗑️ Cleared all notifications');
  },

  // Get current notification count
  count: () => {
    const count = NotificationService.getUnreadCount();
    console.log(`📊 Unread notifications: ${count}`);
    return count;
  },

  // List all notifications
  list: () => {
    const notifications = NotificationService.getNotifications();
    console.log('📋 All notifications:', notifications);
    return notifications;
  },

  // Add a custom test notification
  test: (message = 'Test notification') => {
    NotificationService.addNotification({
      type: 'conflict',
      severity: 'medium',
      title: 'Development Test',
      message,
      actionable: false
    });
    console.log(`✅ Added test notification: ${message}`);
  },

  // Dismiss a specific notification by ID
  dismiss: (id: string) => {
    NotificationService.dismissNotification(id);
    console.log(`🗑️ Dismissed notification: ${id}`);
  },

  // Show available commands
  help: () => {
    console.log(`
🔔 Notification Development Helper
Available commands:
- NotificationDev.addSamples() - Add sample notifications
- NotificationDev.clear() - Clear all notifications  
- NotificationDev.count() - Get unread count
- NotificationDev.list() - List all notifications
- NotificationDev.test(message) - Add custom test notification
- NotificationDev.dismiss(id) - Dismiss specific notification by ID
- NotificationDev.help() - Show this help

Try: NotificationDev.addSamples() to see the notification system in action!
    `);
  }
};

// Make it available globally in development
if (process.env.NODE_ENV === 'development') {
  (window as any).NotificationDev = NotificationDev;
  console.log('🛠️ Notification development helper loaded. Type "NotificationDev.help()" for commands.');
}

export default NotificationDev;
