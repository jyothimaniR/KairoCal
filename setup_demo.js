// Quick Demo Setup Script
// Run this in browser console to set up demo mode with frontend-test-user

console.log('🎭 Setting up demo mode with frontend-test-user...');

// Clear any existing auth
localStorage.removeItem('firebase:authUser:AIzaSyBXXX');

// Set demo mode with frontend-test-user (which has 43 events)
localStorage.setItem('demoMode', 'true');
localStorage.setItem('userEmail', 'demo@kairocal.com');
localStorage.setItem('userCognitoSub', 'frontend-test-user');

console.log('✅ Demo mode configured. Reload the page to see events in MiniCalendar.');
console.log('📅 This will load 43 demo events for testing.');

// Auto-reload after 1 second
setTimeout(() => {
    window.location.reload();
}, 1000);
