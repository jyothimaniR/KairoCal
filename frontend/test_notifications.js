import { NotificationService } from '../src/services/notificationService';

// Test script to verify notification system functionality
console.log('🧪 Testing Notification System...');

// Test 1: Add a test notification
console.log('\n1. Adding test notification...');
NotificationService.addTestNotification();

// Test 2: Check unread count
console.log('Unread count:', NotificationService.getUnreadCount());

// Test 3: Get all notifications
console.log('All notifications:', NotificationService.getNotifications());

// Test 4: Mark as read
const notifications = NotificationService.getNotifications();
if (notifications.length > 0) {
  console.log('\n2. Marking first notification as read...');
  NotificationService.markAsRead(notifications[0].id);
  console.log('Unread count after marking as read:', NotificationService.getUnreadCount());
}

// Test 5: Test smart notification generation with mock data
console.log('\n3. Testing smart notification generation...');
const mockEvents = [
  {
    id: '1',
    title: 'Important Meeting',
    start: new Date(Date.now() + 30 * 60 * 1000), // 30 minutes from now
    end: new Date(Date.now() + 90 * 60 * 1000),
    priority: 9,
    description: 'Critical project discussion'
  },
  {
    id: '2', 
    title: 'Team Standup',
    start: new Date(Date.now() + 2 * 60 * 60 * 1000), // 2 hours from now
    end: new Date(Date.now() + 2.5 * 60 * 60 * 1000),
    priority: 5,
    description: 'Daily team sync'
  }
];

NotificationService.generateSmartNotifications(mockEvents, []);
console.log('Notifications after smart generation:', NotificationService.getNotifications());
console.log('Final unread count:', NotificationService.getUnreadCount());

console.log('\n✅ Notification system test completed!');
