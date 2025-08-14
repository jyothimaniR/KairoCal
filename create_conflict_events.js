/**
 * Script to create conflicting events for testing delete functionality
 */

const API_BASE_URL = 'http://localhost:8000';

async function createConflictingEvents() {
    console.log('🔧 Creating conflicting test events...');
    
    // Get current time and create events at the same time
    const now = new Date();
    const testTime = new Date(now.getTime() + 2 * 60 * 60 * 1000); // 2 hours from now
    const startTime = testTime.toISOString();
    const endTime = new Date(testTime.getTime() + 60 * 60 * 1000).toISOString(); // 1 hour duration
    
    const conflictingEvents = [
        {
            title: "Team Meeting - Conflict Test 1",
            description: "First conflicting event for testing",
            start_time: startTime,
            end_time: endTime,
            priority_level: 2,
            created_via: "manual"
        },
        {
            title: "Project Review - Conflict Test 2", 
            description: "Second conflicting event for testing",
            start_time: startTime, // Same time as first event
            end_time: endTime,
            priority_level: 3,
            created_via: "voice"
        },
        {
            title: "Client Call - Conflict Test 3",
            description: "Third conflicting event for testing", 
            start_time: startTime, // Same time as other events
            end_time: endTime,
            priority_level: 1,
            created_via: "manual"
        }
    ];
    
    console.log(`📅 Creating events at time: ${testTime.toLocaleString()}`);
    
    try {
        for (let i = 0; i < conflictingEvents.length; i++) {
            const event = conflictingEvents[i];
            console.log(`\n${i + 1}. Creating: ${event.title}`);
            
            const response = await fetch(`${API_BASE_URL}/api/v1/events?cognito_sub=test-user-1&auto_classify_priority=true`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(event),
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log(`✅ Created event: ${result.id} - ${result.title}`);
            } else {
                const errorText = await response.text();
                console.error(`❌ Failed to create event: ${response.status} - ${errorText}`);
            }
            
            // Small delay between requests
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        console.log('\n🎉 All conflicting events created successfully!');
        console.log('💡 Refresh your dashboard to see the conflicts and test delete functionality');
        
    } catch (error) {
        console.error('❌ Error creating events:', error);
        console.log('💡 Make sure the backend is running on port 8001');
    }
}

// Also create a function to clean up test events
async function cleanupTestEvents() {
    console.log('🧹 Cleaning up test events...');
    
    try {
        // Get all events
        const response = await fetch(`${API_BASE_URL}/api/v1/events?cognito_sub=test-user-1`);
        if (!response.ok) {
            throw new Error(`Failed to fetch events: ${response.statusText}`);
        }
        
        const events = await response.json();
        const testEvents = events.filter(event => 
            event.title && event.title.includes('Conflict Test')
        );
        
        console.log(`Found ${testEvents.length} test events to clean up`);
        
        for (const event of testEvents) {
            console.log(`🗑️ Deleting: ${event.title}`);
            
            const deleteResponse = await fetch(`${API_BASE_URL}/api/v1/events/${event.id}?cognito_sub=test-user-1`, {
                method: 'DELETE',
            });
            
            if (deleteResponse.ok) {
                console.log(`✅ Deleted: ${event.title}`);
            } else {
                console.error(`❌ Failed to delete: ${event.title}`);
            }
        }
        
        console.log('🎉 Cleanup completed!');
        
    } catch (error) {
        console.error('❌ Error during cleanup:', error);
    }
}

// Check command line arguments
const args = process.argv.slice(2);
if (args.includes('--cleanup')) {
    cleanupTestEvents();
} else {
    createConflictingEvents();
}
