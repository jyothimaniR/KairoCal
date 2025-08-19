// Test script to verify conflict deduplication logic
// This simulates the new frontend conflict detection algorithm

const testEvents = [
  {
    id: "event1",
    title: "Fix High_Priority Server Outage Affecting Customer Database At Aws London Datacenter 4Pm",
    start_time: "2025-08-18T16:00:00.000000",
    end_time: "2025-08-18T18:00:00.000000",
    is_all_day: false,
    priority_level: 5
  },
  {
    id: "event2", 
    title: "Fix Server Crash",
    start_time: "2025-08-18T17:00:00.000000",
    end_time: "2025-08-18T17:45:00.000000",
    is_all_day: false,
    priority_level: 4
  },
  {
    id: "event3",
    title: "Security Breach System Patching With Network Engineers", 
    start_time: "2025-08-19T10:30:00.000000",
    end_time: "2025-08-19T11:30:00.000000",
    is_all_day: false,
    priority_level: 5
  },
  {
    id: "event4",
    title: "Aws Summit Customer Feedback Review With Regional Manager",
    start_time: "2025-08-19T11:00:00.000000", 
    end_time: "2025-08-19T12:30:00.000000",
    is_all_day: false,
    priority_level: 4
  }
];

function testConflictDetection() {
  console.log('🧪 Testing Conflict Deduplication Logic');
  console.log('=====================================');
  
  // Filter out all-day events
  const timeEvents = testEvents.filter(event => !event.is_all_day);
  console.log(`📊 Processing ${timeEvents.length} time-based events`);
  
  // Check for overlapping events using proper pairwise comparison
  const conflictPairs = [];
  
  for (let i = 0; i < timeEvents.length; i++) {
    for (let j = i + 1; j < timeEvents.length; j++) {
      const event1 = timeEvents[i];
      const event2 = timeEvents[j];
      
      const start1 = new Date(event1.start_time);
      const end1 = new Date(event1.end_time);
      const start2 = new Date(event2.start_time);  
      const end2 = new Date(event2.end_time);
      
      console.log(`\n🔄 Checking: "${event1.title}" vs "${event2.title}"`);
      console.log(`   Event 1: ${start1.toLocaleString()} - ${end1.toLocaleString()}`);
      console.log(`   Event 2: ${start2.toLocaleString()} - ${end2.toLocaleString()}`);
      
      // Check for time overlap: events overlap if start1 < end2 AND start2 < end1
      const hasOverlap = start1 < end2 && start2 < end1;
      
      if (hasOverlap) {
        // Calculate overlap details
        const overlapStart = new Date(Math.max(start1.getTime(), start2.getTime()));
        const overlapEnd = new Date(Math.min(end1.getTime(), end2.getTime()));
        const overlapMinutes = Math.round((overlapEnd.getTime() - overlapStart.getTime()) / (1000 * 60));
        
        console.log(`   ⚠️ CONFLICT: ${overlapMinutes} minute overlap`);
        
        conflictPairs.push({
          event1: event1.title,
          event2: event2.title,
          overlapMinutes,
          conflictId: `conflict-${[event1.id, event2.id].sort().join('-')}`
        });
      } else {
        console.log(`   ✅ No conflict`);
      }
    }
  }
  
  console.log(`\n🎯 RESULTS:`);
  console.log(`Found ${conflictPairs.length} unique conflict pairs`);
  
  conflictPairs.forEach((conflict, index) => {
    console.log(`\n  ${index + 1}. ${conflict.conflictId}`);
    console.log(`     "${conflict.event1}" vs "${conflict.event2}"`);
    console.log(`     Overlap: ${conflict.overlapMinutes} minutes`);
  });
  
  console.log(`\n✅ Deduplication Test: ${conflictPairs.length === 2 ? 'PASSED' : 'FAILED'}`);
  console.log(`   Expected: 2 conflicts (Server events + System events)`);
  console.log(`   Actual: ${conflictPairs.length} conflicts`);
  
  return conflictPairs;
}

// Run the test
testConflictDetection();
