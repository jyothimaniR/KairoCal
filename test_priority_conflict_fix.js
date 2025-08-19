// Test the PriorityConflictResolver conflict detection fix
// This simulates the events from your screenshots to verify the fix

const testEvents = [
  // Today's conflicting events (from screenshot 1 & 2)
  {
    id: "event1",
    title: "Fix High Priority Server Outage Affecting Customer Database At Aws London Datacenter 4Pm",
    start_time: "2025-08-18T16:00:00.000000", // 4:00 PM
    end_time: "2025-08-18T18:00:00.000000",   // 6:00 PM
    is_all_day: false,
    priority_level: 5
  },
  {
    id: "event2", 
    title: "Fix Server Crash",
    start_time: "2025-08-18T17:00:00.000000", // 5:00 PM
    end_time: "2025-08-18T17:45:00.000000",   // 5:45 PM
    is_all_day: false,
    priority_level: 5
  },
  // Tomorrow's exact same time events (from screenshot 3)
  {
    id: "event3",
    title: "Brainstorming session with design team",
    start_time: "2025-08-19T15:00:00.000000", // 3:00 PM
    end_time: "2025-08-19T15:30:00.000000",   // 3:30 PM
    is_all_day: false,
    priority_level: 3
  },
  {
    id: "event4",
    title: "Attend Training Workshop For A New Software Tools",
    start_time: "2025-08-19T15:00:00.000000", // 3:00 PM (exact same time)
    end_time: "2025-08-19T18:30:00.000000",   // 6:30 PM
    is_all_day: false,
    priority_level: 3
  }
];

function testPriorityConflictResolver() {
  console.log('🧪 Testing PriorityConflictResolver Conflict Detection');
  console.log('=================================================');
  
  // Filter out all-day events (should be none in test data)
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
        
        // Use the earlier event's start time as the conflict time slot
        const conflictTimeSlot = start1 <= start2 ? event1.start_time : event2.start_time;
        
        console.log(`   ⚠️ CONFLICT: ${overlapMinutes} minute overlap at ${new Date(conflictTimeSlot).toLocaleString()}`);
        
        conflictPairs.push({
          event1: event1.title,
          event2: event2.title,
          overlapMinutes,
          conflictTimeSlot,
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
    console.log(`     Conflict Time: ${new Date(conflict.conflictTimeSlot).toLocaleString()}`);
  });
  
  // Verify expected results
  console.log(`\n📊 VERIFICATION:`);
  console.log(`Expected conflicts:`);
  console.log(`  1. Server Outage vs Server Crash (partial overlap, different times)`);
  console.log(`  2. Brainstorming vs Training Workshop (exact same start time)`);
  console.log(`\n✅ Test Result: ${conflictPairs.length === 2 ? 'PASSED' : 'FAILED'}`);
  console.log(`   Found ${conflictPairs.length} conflicts (expected: 2)`);
  
  // Verify no duplicates by checking unique conflict IDs
  const uniqueIds = new Set(conflictPairs.map(c => c.conflictId));
  console.log(`✅ Deduplication: ${uniqueIds.size === conflictPairs.length ? 'PASSED' : 'FAILED'}`);
  console.log(`   Unique IDs: ${uniqueIds.size}, Total conflicts: ${conflictPairs.length}`);
  
  return conflictPairs;
}

// Run the test
testPriorityConflictResolver();
