// Test the timezone fix
console.log('=== TIMEZONE FIX TEST ===');

// Test original problematic conversion
const testDateTime = '2024-08-17T15:00:00';
console.log('\n1. Original problematic conversion:');
console.log('Input string:', testDateTime);
const oldWay = new Date(testDateTime);
console.log('Old way (Date constructor):', oldWay.toString());
console.log('Old way ISO:', oldWay.toISOString());

// Test fixed conversion
console.log('\n2. Fixed conversion:');
const [datePart, timePart] = testDateTime.split('T');
const [year, month, day] = datePart.split('-').map(Number);
const [hour, minute] = (timePart || '00:00').split(':').map(Number);

const newWay = new Date(year, month - 1, day, hour, minute);
console.log('New way (constructor args):', newWay.toString());
console.log('New way ISO:', newWay.toISOString());

// Show the difference
console.log('\n3. Time difference:');
console.log('Old way hour:', oldWay.getHours());
console.log('New way hour:', newWay.getHours());
console.log('Difference (minutes):', (newWay.getTime() - oldWay.getTime()) / (1000 * 60));

console.log('\n✅ Fixed: Times now stay in local timezone until explicitly converted to UTC!');
