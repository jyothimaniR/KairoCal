/**
 * Debug script to understand conflicts issues
 * Date: August 17, 2025 (Sunday)
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

async function debugCurrentState() {
    console.log('🔍 DEBUGGING CONFLICTS ISSUES');
    console.log('Current date:', new Date().toDateString()); // Should show Sunday Aug 17, 2025
    console.log('='.repeat(50));
    
    try {
        // 1. Check existing events
        console.log('\n📅 EXISTING EVENTS:');
        const events = await fetch(`${API_BASE_URL}/api/v1/events?cognito_sub=test-user-1`);
        const eventsList = await events.json();
        
        eventsList.forEach((event, i) => {
            const startDate = new Date(event.start_time);
            const endDate = new Date(event.end_time);
            console.log(`${i + 1}. ${event.title}`);
            console.log(`   Date: ${startDate.toDateString()} (${startDate.getDay() === 0 ? 'Sunday' : startDate.getDay() === 1 ? 'Monday' : 'Other'})`);
            console.log(`   Time: ${startDate.toLocaleTimeString()} - ${endDate.toLocaleTimeString()}`);
            console.log(`   Full: ${event.start_time} to ${event.end_time}`);
            console.log('');
        });
        
        // 2. Test conflict detection on one event
        console.log('\n🚨 TESTING CONFLICT DETECTION:');
        if (eventsList.length > 0) {
            const testEvent = eventsList[0];
            console.log(`Testing conflicts for: ${testEvent.title}`);
            
            const payload = {
                title: testEvent.title,
                start_time: testEvent.start_time,
                end_time: testEvent.end_time,
                description: testEvent.description || '',
                is_all_day: testEvent.is_all_day || false
            };
            
            const conflictResponse = await fetch(`${API_BASE_URL}/api/v1/conflicts/check?cognito_sub=test-user-1`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (conflictResponse.ok) {
                const conflicts = await conflictResponse.json();
                console.log('Conflicts found:', conflicts.conflicts?.length || 0);
                if (conflicts.conflicts?.length > 0) {
                    conflicts.conflicts.forEach((conflict, i) => {
                        console.log(`  ${i + 1}. ${conflict.description}`);
                        console.log(`     Severity: ${conflict.severity}`);
                    });
                }
            } else {
                console.log('Error checking conflicts:', await conflictResponse.text());
            }
        }
        
        // 3. Create proper test conflicts for TODAY (Sunday)
        console.log('\n📝 CREATING TEST CONFLICTS FOR TODAY (SUNDAY):');
        const todayAt9AM = new Date();
        todayAt9AM.setHours(9, 0, 0, 0);
        
        const todayAt930AM = new Date();
        todayAt930AM.setHours(9, 30, 0, 0);
        
        if (todayAt9AM > new Date()) {
            console.log('Cannot create events in the past - 9AM today has passed');
        } else {
            console.log(`Creating events for today: ${todayAt9AM.toDateString()}`);
        }
        
        const conflictEvents = [
            {
                title: 'Sunday Morning Meeting',
                description: 'Test conflict event for today',
                start_time: '2025-08-17T09:00:00',
                end_time: '2025-08-17T10:00:00',
                priority_level: 3
            },
            {
                title: 'Sunday Coffee Break',
                description: 'Overlapping with morning meeting',
                start_time: '2025-08-17T09:30:00',
                end_time: '2025-08-17T10:30:00',
                priority_level: 2
            }
        ];
        
        for (const event of conflictEvents) {
            console.log(`Creating: ${event.title} at ${event.start_time}`);
            const response = await fetch(`${API_BASE_URL}/api/v1/events?cognito_sub=test-user-1&auto_classify_priority=true`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(event)
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log(`✅ Created: ${result.id}`);
            } else {
                const error = await response.text();
                console.log(`❌ Failed: ${error}`);
            }
        }
        
    } catch (error) {
        console.error('❌ Debug error:', error);
    }
}

debugCurrentState();
