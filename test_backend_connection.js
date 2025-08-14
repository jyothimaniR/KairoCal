/**
 * Simple test to check backend connectivity and API endpoints
 */

const API_BASE_URL = 'http://localhost:8000';

async function testBackendConnection() {
    console.log('🔍 Testing KairoCal Backend Connection...');
    console.log('Backend URL:', API_BASE_URL);
    
    try {
        // Test health endpoint
        console.log('\n1. Testing health endpoint...');
        const healthResponse = await fetch(`${API_BASE_URL}/health`);
        console.log('Health status:', healthResponse.status);
        if (healthResponse.ok) {
            const healthData = await healthResponse.json();
            console.log('Health data:', healthData);
        }
        
        // Test events endpoint
        console.log('\n2. Testing events endpoint...');
        const eventsResponse = await fetch(`${API_BASE_URL}/api/v1/events?cognito_sub=test-user-1`);
        console.log('Events status:', eventsResponse.status);
        if (eventsResponse.ok) {
            const events = await eventsResponse.json();
            console.log('Events count:', events.length);
            console.log('Sample event:', events[0]);
            
            // Test updating priority on the first event
            if (events.length > 0) {
                const testEvent = events[0];
                console.log('\n3. Testing priority update...');
                console.log('Target event:', testEvent.id, testEvent.title);
                
                const updateResponse = await fetch(`${API_BASE_URL}/api/v1/events/${testEvent.id}?cognito_sub=test-user-1`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        priority_level: 2
                    }),
                });
                
                console.log('Update status:', updateResponse.status);
                if (updateResponse.ok) {
                    const updateResult = await updateResponse.json();
                    console.log('Update result:', updateResult);
                } else {
                    const errorText = await updateResponse.text();
                    console.log('Update error:', errorText);
                }
            }
        } else {
            const errorText = await eventsResponse.text();
            console.log('Events error:', errorText);
        }
        
    } catch (error) {
        console.error('❌ Connection failed:', error.message);
        console.log('💡 Make sure the backend is running on port 8001');
    }
}

// Run the test
testBackendConnection();
