// More comprehensive timezone test
console.log('=== COMPREHENSIVE TIMEZONE TEST ===');

// Current timezone info
const now = new Date();
console.log('Current time:', now.toString());
console.log('Timezone offset (minutes):', now.getTimezoneOffset());
console.log('UTC time:', now.toUTCString());

// Test different scenarios
const testScenarios = [
  '2024-08-17T15:00:00',     // No timezone
  '2024-08-17T15:00:00Z',    // UTC timezone
  '2024-08-17T15:00:00+01:00' // Explicit BST
];

console.log('\n=== SCENARIO TESTS ===');
testScenarios.forEach((scenario, i) => {
  console.log(`\n${i + 1}. Testing: "${scenario}"`);
  
  // Method 1: Date constructor
  const date1 = new Date(scenario);
  console.log('  Date constructor:', date1.toString());
  console.log('  As ISO:', date1.toISOString());
  
  // Method 2: Parse and reconstruct (our fix)
  if (!scenario.includes('Z') && !scenario.includes('+')) {
    const [datePart, timePart] = scenario.split('T');
    const [year, month, day] = datePart.split('-').map(Number);
    const [hour, minute] = (timePart || '00:00').split(':').map(Number);
    
    const date2 = new Date(year, month - 1, day, hour, minute);
    console.log('  Fixed method:', date2.toString());
    console.log('  As ISO:', date2.toISOString());
    
    const diff = Math.abs(date1.getTime() - date2.getTime()) / (1000 * 60);
    console.log(`  Difference: ${diff} minutes`);
  }
});

// Test what the API would receive
console.log('\n=== API SIMULATION ===');
const inputTime = '2024-08-17T15:00:00';
const oldMethod = new Date(inputTime).toISOString();
const [datePart, timePart] = inputTime.split('T');
const [year, month, day] = datePart.split('-').map(Number);
const [hour, minute] = (timePart || '00:00').split(':').map(Number);
const newMethod = new Date(year, month - 1, day, hour, minute).toISOString();

console.log('User expects 3:00 PM local time');
console.log('Old method sends to API:', oldMethod, '(backend sees this as', new Date(oldMethod).toString(), ')');
console.log('New method sends to API:', newMethod, '(backend sees this as', new Date(newMethod).toString(), ')');
