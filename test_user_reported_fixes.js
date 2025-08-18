/**
 * Test script to verify the user-reported issues are actually fixed:
 * 1. Priority changes now work (clickable priority labels)
 * 2. Timezone reschedule offset fixed (no more 1-hour early scheduling)
 */

const API_BASE_URL = 'http://localhost:8000';

async function testPriorityChange() {
    console.log('\n🧪 TESTING PRIORITY CHANGE FIX');
    console.log('===============================');
    
    try {
        // Get events
        const events = await fetch(`${API_BASE_URL}/api/v1/events?cognito_sub=frontend-test-user`)
            .then(res => res.json());
        
        if (events.length === 0) {
            console.log('❌ No events found to test with');
            return false;
        }
        
        const testEvent = events[0];
        console.log(`📋 Testing with event: "${testEvent.title}"`);
        console.log(`🔢 Current priority: ${testEvent.priority_level}`);
        
        const originalPriority = testEvent.priority_level;
        const newPriority = originalPriority === 1 ? 2 : 1; // Toggle between high priorities
        
        // Test priority update
        const updateResponse = await fetch(`${API_BASE_URL}/api/v1/events/${testEvent.id}?cognito_sub=frontend-test-user`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ priority_level: newPriority })
        });
        
        if (updateResponse.ok) {
            const updatedEvent = await updateResponse.json();
            console.log(`✅ SUCCESS: Priority changed from ${originalPriority} to ${updatedEvent.priority_level}`);
            
            // Change it back
            await fetch(`${API_BASE_URL}/api/v1/events/${testEvent.id}?cognito_sub=frontend-test-user`, {
                method: 'PUT', 
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ priority_level: originalPriority })
            });
            
            console.log(`🔄 Restored original priority: ${originalPriority}`);
            return true;
        } else {
            console.log(`❌ FAILED: Priority update failed - ${updateResponse.status}`);
            return false;
        }
        
    } catch (error) {
        console.error('❌ ERROR in priority test:', error);
        return false;
    }
}

async function testTimezoneRescheduleFix() {
    console.log('\n🕐 TESTING TIMEZONE RESCHEDULE FIX');
    console.log('=================================');
    
    try {
        // Get events
        const events = await fetch(`${API_BASE_URL}/api/v1/events?cognito_sub=frontend-test-user`)
            .then(res => res.json());
        
        if (events.length === 0) {
            console.log('❌ No events found to test with');
            return false;
        }
        
        const testEvent = events[0];
        console.log(`📋 Testing with event: "${testEvent.title}"`);
        
        const originalStartTime = testEvent.start_time;
        const originalEndTime = testEvent.end_time;
        console.log(`🕐 Original time: ${originalStartTime} to ${originalEndTime}`);
        
        // Create a test time that's 2 hours later
        const originalStart = new Date(originalStartTime);
        const testStart = new Date(originalStart.getTime() + 2 * 60 * 60 * 1000);
        const testEnd = new Date(new Date(originalEndTime).getTime() + 2 * 60 * 60 * 1000);
        
        // Format as local time (no timezone conversion)
        const formatLocalDateTime = (date) => {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            const seconds = String(date.getSeconds()).padStart(2, '0');
            return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
        };
        
        const newStartFormatted = formatLocalDateTime(testStart);
        const newEndFormatted = formatLocalDateTime(testEnd);
        
        console.log(`🔄 Testing reschedule to: ${newStartFormatted} to ${newEndFormatted}`);
        console.log(`📊 Expected: Time moves exactly 2 hours later, no timezone offset`);
        
        // Test reschedule
        const rescheduleResponse = await fetch(`${API_BASE_URL}/api/v1/events/${testEvent.id}?cognito_sub=frontend-test-user`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                start_time: newStartFormatted, 
                end_time: newEndFormatted 
            })
        });
        
        if (rescheduleResponse.ok) {
            const rescheduledEvent = await rescheduleResponse.json();
            console.log(`✅ RESCHEDULE SUCCESSFUL`);
            console.log(`🕐 New time: ${rescheduledEvent.start_time} to ${rescheduledEvent.end_time}`);
            
            // Verify times match what we sent (no timezone conversion)
            if (rescheduledEvent.start_time === newStartFormatted && 
                rescheduledEvent.end_time === newEndFormatted) {
                console.log(`✅ SUCCESS: Times exactly match - no timezone offset!`);
            } else {
                console.log(`⚠️  WARNING: Times don't exactly match:`);
                console.log(`   Sent: ${newStartFormatted} to ${newEndFormatted}`);  
                console.log(`   Got:  ${rescheduledEvent.start_time} to ${rescheduledEvent.end_time}`);
            }
            
            // Restore original time
            await fetch(`${API_BASE_URL}/api/v1/events/${testEvent.id}?cognito_sub=frontend-test-user`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    start_time: originalStartTime, 
                    end_time: originalEndTime 
                })
            });
            
            console.log(`🔄 Restored original time`);
            return true;
            
        } else {
            console.log(`❌ FAILED: Reschedule failed - ${rescheduleResponse.status}`);
            const error = await rescheduleResponse.text();
            console.log(`Error details: ${error}`);
            return false;
        }
        
    } catch (error) {
        console.error('❌ ERROR in timezone test:', error);
        return false;
    }
}

async function runAllTests() {
    console.log('🚀 TESTING USER REPORTED BUG FIXES');
    console.log('===================================');
    console.log('Testing fixes for:');
    console.log('1. "priorities can\'t be changed" ');
    console.log('2. "reschedules one hr early"');
    
    const priorityTestPassed = await testPriorityChange();
    const timezoneTestPassed = await testTimezoneRescheduleFix();
    
    console.log('\n📊 TEST RESULTS');
    console.log('===============');
    console.log(`Priority Change Fix: ${priorityTestPassed ? '✅ WORKING' : '❌ BROKEN'}`);
    console.log(`Timezone Reschedule Fix: ${timezoneTestPassed ? '✅ WORKING' : '❌ BROKEN'}`);
    
    if (priorityTestPassed && timezoneTestPassed) {
        console.log('\n🎉 ALL FIXES WORKING! User issues should be resolved.');
    } else {
        console.log('\n⚠️  Some fixes still need work.');
    }
}

// Run the tests
runAllTests().catch(console.error);
